from django.urls import path
from . import views

app_name = 'Buyer'

# N0ur@123

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='Search'),
    path("products/", views.products, name="Products"),
    path("productdetails/<int:prid>", views.productdetails, name="productdetails"),
    path("addtocart/<int:prid>", views.addtocart, name="Addtocart"),
    path("deletefromcart/<int:prid>", views.deletefromcart, name="Deletefromcart"),
    path("cart/", views.cart, name="cart"),
    path("clearcart/", views.clearcart, name="clearcart"),
    path("checkout/", views.checkout, name="Checkout"),
    path("account/updateprofile/", views.updateProfile, name="UpdateProfile"),
]
