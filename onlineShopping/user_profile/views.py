from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import EditProfileForm
def view_profile(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'user_profile/view_profile.html', {'user': user})
    else:
        return redirect('/')  

def edit_profile(request):
    user = request.user
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            # Add other fields as needed
            user.save()
            return redirect('/user_profile/')
    else:
        form = EditProfileForm(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            # Add other fields as needed
        })
    
    return render(request, 'user_profile/edit_profile.html', {'form': form})