from django.shortcuts import *
from admins.models import admins
from main.models import Product
from userapp.models import Order
from django.db.models import Sum

# Create your views here.

def all_users(request):
    return render(request, 'dashboard.html')

def admin_login_page(request):
    return render(request, 'admin_login.html')

def admin_dash(request):
    return render(request, 'admin_dash.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        from admins.models import admins
        try:
            existing_admin = admins.objects.get(email=email, password=password)
            return render(request, 'admin_dash.html', {'adminname': existing_admin.adminname})
        
        except admins.DoesNotExist:
            return render(request, 'admin_login.html', {'error': 'Invalid email or password.'})
    return render(request, 'admin_login.html')

def all_users(request):
    from userapp.models import user
    users = user.objects.all()
    return render(request, 'all_users.html', {'users': users})

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        desc = request.POST['description']
        img = request.FILES.get('image') 

        # Creating the product in the database
        Product.objects.create(
            name=name, 
            price=price, 
            description=desc, 
            image=img 
        )
        # Redirect back to the same page to see the updated table
        return redirect('add_product') 

    # This part handles the 'GET' request (loading the page)
    # You MUST fetch products here so the table in add_product.html isn't empty
    products = Product.objects.all() 
    return render(request, 'add_product.html', {'products': products})

def view_orders(request):
    orders = Order.objects.all()
    return render(request, 'view_orders.html', {'orders': orders})

def sale_report(request):
    total_sales = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = Order.objects.count()
    return render(request, 'sale_report.html', {
        'total_sales': total_sales,
        'total_orders': total_orders
    })

def logout(request):
    # This removes the admin_id and logs the admin out
    request.session.flush() 
    return redirect('admin_login_page')

def update_order_status(request, order_id):
    order_obj = Order.objects.get(id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order_obj.status = new_status
        order_obj.save()
        return redirect('view_orders')
    return render(request, 'update_status.html', {'order': order_obj})

def delete_product(request, product_id):
    # Retrieve and delete the specific product
    product_obj = Product.objects.get(id=product_id)
    product_obj.delete()
    return redirect('add_product')

def update_product(request, product_id):
    product_obj = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product_obj.name = request.POST.get('name')
        product_obj.price = request.POST.get('price')
        
        # Ensure 'description' is captured. Adding '' as a default 
        # prevents the 'null' database error if the field is somehow missed.
        product_obj.description = request.POST.get('description', '') 
        
        if request.FILES.get('image'):
            product_obj.image = request.FILES['image']
            
        product_obj.save()
        return redirect('add_product')
        
    return render(request, 'update_product.html', {'product': product_obj})
def update_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order_obj = Order.objects.get(id=order_id)
        order_obj.status = new_status
        order_obj.save()
        return redirect('view_orders')