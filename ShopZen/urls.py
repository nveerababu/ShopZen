"""
URL configuration for ShopZen project.

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
from django.urls import path,include
from testapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Admin dashboard (staff only)
    path('dashboard/', views.dashboard_view, name='dashboard'),

    #login page view
    path('accounts/',include('django.contrib.auth.urls')),

    #signup page view
    path('signup/',views.signupform_view),

    #logout pager view
    path('logout/',views.logout_view),

    #about page view
    path('about/',views.aboutpage_view),

    #conatct page view
    path('contactus/',views.conatctpage_view),

    #updates page view
    path('updates/',views.updatespage_view),

    # Add to Cart
    path('add-to-cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),

    # Cart Page
    path('cart/', views.cart_view, name='cart'),



    #buynow page

     path('buynow/<int:product_id>/',views.buy_now, name='buy_now'),
     path('checkout/',views.checkout_cart, name='checkout_cart'),
     path('ordersuccess/',views.order_success, name='order_success'),


    # Navbar and Homepage
    path('navbar/', views.navbar_view, name='navbar'),
    path('', views.homepage_view, name='home'),

    # Product CRUD
    path('product/add/',
         views.ProductCreateView.as_view(), name='product_add'),

    path('product/<int:id>/update/',
         views.ProductUpdateView.as_view(), name='product_update'),

    path('product/<int:id>/delete/',
         views.ProductDeleteView.as_view(), name='product_delete'),
]
