from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
]
