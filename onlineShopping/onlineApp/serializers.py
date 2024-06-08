from rest_framework import serializers
from .models import Brands, Products
from django.contrib.auth.models import User


class AddProductFormSerializer(serializers.ModelSerializer):
    brand = serializers.ChoiceField(choices=[(
        stype.brand_type, stype.brand_title) for stype in Brands.objects.all()])

    class Meta:
        model = Products
        fields = ['product_name', 'product_desc', 'product_price',
                  'brand', 'product_image']

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid()
        product = self.initial_data.get('product_name')
        if is_valid:
            if Products.objects.filter(product_name=product).exists():
                self.errors['product_name'] = ['title should be unique']
                if raise_exception:
                    raise serializers.ValidationError(self.errors)
                return False
        return is_valid

    def create(self, validated_data):
        product = Products.objects.create(**validated_data)
        return product

