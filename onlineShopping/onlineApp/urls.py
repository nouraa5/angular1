from django.urls import path, include
from . import views, api_views
app_name='onlineApp'

urlpatterns = [
    path('add-product-form/', api_views.AddProductFormView.as_view(),
         name='add_product_form'),
    path('search-product/', api_views.search_product,
         name='search_product'),
    path('user-profile', api_views.get_user_profile, name='get_user_profile'),
    path('user-profile-update', api_views.update_user_profile,
         name='update_user_profile'),
    path('products/<int:product_id>/title',
         api_views.get_product_name, name='get_product_name'),
    path('my-products/<int:id>/',
         api_views.get_myProducts, name='get_myProducts'),
    path('edit-product/<int:product_id>/',
         api_views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/',
         api_views.delete_product, name='delete_product'),
    path('user-info/', api_views.user_info, name='user_info'),
    path('', views.search_product, name='search_product'),
    path('add_product', views.add_product, name='add_product'),
    path('my_products', views.my_products, name='my_products'),
    path('edit-product/<int:product_id>/',
         views.edit_product, name='edit_product]'),
    path('delete-product/<int:product_id>/',
         views.delete_product, name='delete_product'),
#     path('product_details/<int:product_id>',
#          views.product_details, name='product_details')  # under development could be a function
]
