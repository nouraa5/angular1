from django.contrib import admin

# Register your models here.
from buyer.models import Orders, OrderProduct, Cart, Customer


admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(OrderProduct)
