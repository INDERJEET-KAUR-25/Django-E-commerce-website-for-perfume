from django.shortcuts import *
from main.models import Product


# Create your views here.
def home(request):
    return render(request,'home.html')


def collection(request):
    products = Product.objects.all()
    return render(request,'collection.html',{'products':products})

def contact(request):
    return render(request,'contact.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')