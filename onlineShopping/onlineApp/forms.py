from django import forms
from .models import Brands, Products

class SearchForm(forms.Form):
    brand_title = forms.ModelChoiceField(
        queryset=Brands.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'brand-dropdown'}),
        label="Brand",
    )
    custom_text = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'custom-text', 'placeholder': 'Enter your product name'})
    )


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'product_price',
                  'brand', 'product_desc', 'product_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['product_name'].label = ''
        self.fields['product_name'].widget.attrs['placeholder'] = 'Enter your Product Name'
        self.fields['product_desc'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['product_desc'].label = ''
        self.fields['product_desc'].widget.attrs['placeholder'] = 'Enter your Product description'
        self.fields['product_price'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['product_price'].label = ''
        self.fields['product_price'].widget.attrs['placeholder'] = 'Enter your Product price'
        self.fields['brand'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['brand'].label = ''
        self.fields['product_image'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['product_image'].label = ''


class EditProfileForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['last_name'].label = 'Last Name'


