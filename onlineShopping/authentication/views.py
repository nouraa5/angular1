from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .forms import login_form, RegistrationForm, changePasswordForm

@api_view(['POST'])
def loginUser(request):
    if request.user.is_authenticated:
        return Response({'detail': 'Already authenticated'}, status=status.HTTP_400_BAD_REQUEST)

    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        return Response({'detail': 'Login successful'})
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logoutUser(request):
    logout(request)
    return Response({'detail': 'Logout successful'})

@api_view(['POST'])
def signup(request):
    form = RegistrationForm(request.data)
    if form.is_valid():
        user = form.save()
        group = form.cleaned_data['group']
        user.groups.add(group)
        login(request, user)
        return Response({'detail': 'Registration successful'})
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def changePassword(request):
    form = changePasswordForm(request.data)
    if form.is_valid():
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        try:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            return Response({'detail': 'Password changed successfully'})
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
