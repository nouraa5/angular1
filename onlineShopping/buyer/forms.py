from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from buyer.models import Customer
from onlineApp.models import Brands


class SearchForm(forms.Form):
    brand_title = forms.ModelChoiceField(
        queryset=Brands.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'brand-dropdown'}),
        label="Brand"
    )
    custom_text = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'custom-text'})
    )


class CheckoutForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))
    mobile = forms.CharField(label='Mobile', max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}))
    city = forms.CharField(label='City', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your city'}))
    state = forms.CharField(label='State', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your state'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'mobile': 'Enter your mobile number',
            'city': 'Enter your city',
            'state': 'Enter your state',
            'email': 'Enter your email address',
        }
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control', 'placeholder': placeholders.get(field, '')})


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, required=True)  # Add first_name field
    last_name = forms.CharField(
        max_length=30, required=True)   # Add last_name field
    email = forms.EmailField(
        max_length=254, required=True)     # Add email field

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name',
                  'email', 'mobile', 'state', 'city')

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email'})
        self.fields['mobile'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Mobile Number'})
        self.fields['state'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'State'})
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'City'})

    def clean(self):
        cleaned_data = super().clean()
