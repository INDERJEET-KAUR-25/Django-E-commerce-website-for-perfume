"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from userapp import views as user_views
from django.conf.urls.static import static
from django.conf import settings
from admins import views as admin_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('collection/',views.collection,name='collection'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('add_user/',user_views.add_user,name='add_user'),
    path('user_login/',user_views.user_login,name='user_login'),
    path('admin_login_page/',admin_views.admin_login_page,name='admin_login_page'),
    path('admin_login/',admin_views.admin_login,name='admin_login'),
    path('all_users/',admin_views.all_users,name='all_users'),
    path('admin_dash/',admin_views.admin_dash,name='admin_dash'),
    path('otp_login/',user_views.otp_login,name='otp_login'),
    path('verify_otp/',user_views.verify_otp,name='verify_otp'),
    path('send_otp/',user_views.send_otp,name='send_otp'),
    path('generate_otp/',user_views.generate_otp,name='generate_otp'),
    path('place_order/<int:product_id>/',user_views.place_order,name='place_order'),
    path('my_orders/',user_views.my_orders,name='my_orders'),
    path('add_product/',admin_views.add_product,name='add_product'),
    path('view_orders/',admin_views.view_orders,name='view_orders'),
    path('sale_report/',admin_views.sale_report,name='sale_report'),
    path('see_products/',user_views.see_products,name='see_products'),
    path('logout/',user_views.logout,name='logout'),
    path('admin_logout/',admin_views.logout,name='admin_logout'),
    path('delete_product/<int:product_id>/',admin_views.delete_product,name='delete_product'),
    path('update_product/<int:product_id>/',admin_views.update_product,name='update_product'),
    path('update_order_status/<int:order_id>/',admin_views.update_order_status,name='update_order_status'),
    path('update-status/<int:order_id>/', admin_views.update_status, name='update_status'),
    path('home/', user_views.home, name='home'),
    path('profile/', user_views.user_profile, name='profile'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
