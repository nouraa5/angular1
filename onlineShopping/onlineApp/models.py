from django.db import models
from django.contrib.auth.models import User

class Brands(models.Model):
    brand_type = models.CharField(primary_key=True, max_length=20)
    brand_title = models.CharField(max_length=150)
    
    def __str__(self):
        return self.brand_title

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)  # Changed to AutoField
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=150)
    product_price = models.DecimalField(max_digits=15, decimal_places=2)  # Changed to DecimalField
    product_desc = models.CharField(max_length=150)
    product_image = models.ImageField(null=True, blank=True, upload_to="images/")
    product_keywords = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name
