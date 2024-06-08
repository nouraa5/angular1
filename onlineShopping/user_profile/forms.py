from django import forms

class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['username'].label = 'Username'
        self.fields['email'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control border border-dark border-1'
        self.fields['last_name'].label = 'Last Name'
