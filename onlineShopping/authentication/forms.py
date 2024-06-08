from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User, Group



class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control border border-dark border-1', 'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control border border-dark border-1', 'placeholder': 'Your First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control border border-dark border-1', 'placeholder': 'Your Last Name'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control border border-dark border-1', 'placeholder': 'Your Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control border border-dark border-1', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control border border-dark border-1', 'placeholder': 'Repeat your password'}))
    group = forms.ModelChoiceField(queryset=Group.objects.filter(name__in=['Seller', 'Buyer']), widget=forms.Select(attrs={'class': 'form-control border border-dark border-1'}))

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2', 'group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class login_form(forms.Form):
    email = forms.EmailField(label='', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Your Email'}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'type':'password', 'placeholder': 'Your Password'}))


class changePasswordForm(forms.Form):
    email = forms.CharField(label="Email:", max_length=100, widget=forms.TextInput(attrs={'class':'form-control border border-dark border-1', 'placeholder':'Email'}))
    password1 = forms.CharField(label="Password", max_length=100, validators=[validate_password], widget=forms.PasswordInput(
        attrs={'class': 'form-control border border-dark border-1', 'type': 'password','placeholder':'Password'}))
    password2 = forms.CharField(label="Confirm Password", max_length=100, widget=forms.PasswordInput(
        attrs={'class': 'form-control text-dark', 'type': 'password','placeholder':'Confirm Password'}))
    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not email or not password1 or not password2:
            raise forms.ValidationError('All fields are required.')
        if password2 != password1:
            raise forms.ValidationError('Passwords is not confirmed')
        return super().clean()