from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView,activate,UserLoginView,UserLogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('active/<uid64>/<token>/',activate,name='active'),
]
