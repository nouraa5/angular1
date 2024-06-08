from django.db import models
from django.contrib.auth.models import User
from onlineApp.models import Products
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    mobile = models.CharField(max_length=8)
    city = models.CharField(null=True, max_length=20)
    state = models.CharField(null=True, max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE,  null=True)
    qty = models.IntegerField()

    @property
    def price(self):
        return self.product.product_price

    @property
    def amount(self):
        return self.qty * self.product.product_price

    def __str__(self):
        return f"{self.product.product_name} by {self.user.username}"

STATUS = (
    ('Placed', 'Placed'),
    ('Confirmed', 'Confirmed'),
    ('Preparing', 'Preparing'),
    ('Shipped', 'Shipped'),
    ('Out For Delivery', 'Out For Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=10, null=True)
    last_name = models.CharField(max_length=10)
    mobile = models.BigIntegerField(null=True)
    city = models.CharField(max_length=200, null=True, blank=False)
    state = models.CharField(max_length=200, null=True, blank=False)
    total_amt = models.FloatField()
    
    def __str__(self):
        return f"{self.code} to {self.first_name} {self.last_name}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    qty = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='Placed')

    def __str__(self):
        return f"{self.product.product_name} by {self.user.first_name}"
