from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('list', views.RentAdvertisementViewSet)
router.register('rent_request',views.RentRequestViewSet)
router.register('favourite', views.FavouriteViewSet)
router.register('reviews',views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]