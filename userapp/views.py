from django.shortcuts import *
from main.models import Product
from userapp.models import Order, Order, user
from django.core.mail import send_mail
from shop import settings
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def generate_otp():
    otp = ""
    for _ in range(6):
        otp += str(random.randint(0,9))
    return otp

# Create your views here.
def register(request):
    return render(request, 'register.html')

def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        profile = request.FILES.get('profile')

        otp = generate_otp()

        from userapp.models import user
        new_user = user(username=username, 
                        email=email,
                        password=password,
                        OTP=otp, 
                        profile=profile)
        
        send_mail(
            'Welcome to Shop',
            f'Hi {username}, welcome to our shop! Thank you for registering.\n We are excited to have you with us. Happy shopping!\n Regards,\n LUXE Shop Team',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        new_user.save()

        return render(request, 'register.html', {'message': 'User registered successfully!'})
    
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        from userapp.models import user
        try:
            existing_user = user.objects.get(email=email, password=password)
            request.session['user_id'] = existing_user.id
            return render(request, 'home.html', {'username': existing_user.username})
        
        except user.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
        return render(request, 'login.html')


def otp_login(request):
    return render(request, 'otp_login.html')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        from userapp.models import user
        try:
            existing_user = user.objects.get(email=email)
            otp = generate_otp()
            existing_user.OTP = otp
            existing_user.save()

            send_mail(
                'Your OTP for Login',
                f'Hi {existing_user.username}, your OTP for login is: {otp}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return render(request, 'verify_otp.html', {'email': email, 'message': 'OTP sent to your email.'})
        
        except user.DoesNotExist:
            return render(request, 'otp_login.html', {'error': 'Email not registered.'})
    return render(request, 'otp_login.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        entered_otp = request.POST['otp']

        from userapp.models import user
        try:
            existing_user = user.objects.get(email=email)
            if existing_user.OTP == entered_otp:
                request.session['user_id'] = existing_user.id
                existing_user.OTP = ''
                existing_user.save()
                return render(request, 'home.html', {'username': existing_user.username})
            else:
                return render(request, 'verify_otp.html', {'email': email, 'error': 'Invalid OTP. Please try again.'})
        
        except user.DoesNotExist:
            return render(request, 'otp_login.html', {'error': 'Email not registered.'})
    return render(request, 'otp_login.html')

def place_order(request, product_id):
    product_obj = Product.objects.get(id=product_id)
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')
        
    if request.method == 'POST':
        address = request.POST.get('address')
        customer = user.objects.get(id=user_id)
        
        Order.objects.create(
            user=customer, 
            product=product_obj, # This must match the field in models.py
            total_price=product_obj.price,
            address=address,
            status="Pending"
        )
        return render(request, 'profile.html', {'message': 'Order placed successfully!'})
        
    return render(request, 'place_order.html', {'product': product_obj})
def my_orders(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    # Filter orders so the user only sees their own history
    orders = Order.objects.filter(user_id=user_id).order_by('-id')
    return render(request, 'my_orders.html', {'orders': orders})

def see_products(request):
    products = Product.objects.all()
    return render(request, 'collection.html', {'products': products})

def logout(request):
    # This removes the user_id and logs the user out
    request.session.flush() 
    return redirect('home')

def home(request):
    # Django templates can access request.session directly, 
    # but you can also pass the username to personalize the welcome message.
    user_id = request.session.get('user_id')
    context = {}
    
    if user_id:
        from userapp.models import user
        current_user = user.objects.get(id=user_id)
        context['username'] = current_user.username
        
    return render(request, 'home.html', context)

def user_profile(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    # Fetch the specific user instance
    current_user = user.objects.get(id=user_id)
    return render(request, 'profile.html', {'curr_user': current_user})

