from django.urls import path
from .api_views import login_view, SignupFormView, logout_view, ChangePasswordView, get_csrf_token, user_info

app_name = 'authentication'


urlpatterns = [
    # path('signup/', SignupView.as_view(), name='api_signup'),
    path('login/', login_view, name='api_login'),
    path('logout/', logout_view, name='api_logout'),
    path('user-info/', user_info, name='user_info'),
    path('signup-form/', SignupFormView.as_view(), name='signup_form'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('change-password/', ChangePasswordView,
         name='change_password'),
]
