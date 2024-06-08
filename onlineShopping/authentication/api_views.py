from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, ChangePasswordSerializer, SignupFormSerializer
from django.db import IntegrityError


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


@method_decorator(csrf_exempt, name='dispatch')
class SignupFormView(APIView):

    def get(self, request, *args, **kwargs):
        form = SignupForm()

        # Initialize the form data
        form_data = {
            'username': form['username'].value() or '',
            'first_name': form['first_name'].value() or '',
            'last_name': form['last_name'].value() or '',
            'email': form['email'].value() or '',
            'password1': form['password1'].value() or '',
            'password2': form['password2'].value() or '',
            'group': form['group'].value() or '',
        }

        # Initialize the serializer with the form data
        form_serializer = SignupFormSerializer(data=form_data)

        # Validate the serializer to prepare the choices
        form_serializer.is_valid(raise_exception=False)

        # Prepare the response data
        response_data = {
            'initial_data': form_serializer.initial_data,
            'choices': {
                'group': [{'id': group.id, 'name': group.name} for group in Group.objects.filter(name__in=['Seller', 'Buyer'])]
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        form_serializer = SignupFormSerializer(data=request.data['data'])
        # print(form_serializer)
        if form_serializer.is_valid():
            try:
                user = form_serializer.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'username': ['This username is already taken.']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(form_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            user = User.objects.get(Q(email=email))
        except User.DoesNotExist:
            user = None

        if user is not None:
            if user.check_password(password):
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': ['Invalid credentials']}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': ['Invalid credentials']}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def ChangePasswordView(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            # print(username)
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            return Response({'message': 'password changed successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'username': ['Invalid credentials']}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def user_info(request):
    user = request.user
    is_seller = user.groups.filter(name='Seller').exists()
    data = {
        'userid': user.id,
        'username': user.username,
        'is_seller': is_seller
    }
    return JsonResponse(data)
