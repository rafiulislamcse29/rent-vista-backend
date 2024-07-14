from django.shortcuts import render
from rest_framework import viewsets,filters
from .models import RentAdvertisement,RentRequest,Favourite,Review
from .serializers import RentAdvertisementSerializer,RentRequestSerializer,FavouriteSerializer,ReviewSerializer

from django.db.models import Q 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOfAdvertisement
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class RentAdvertisementOwner(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    owner_id=request.query_params.get('owner_id')
    if owner_id :
      print( query_set.filter(owner=owner_id ))
    return query_set
         

class RentAdvertisementViewSet(viewsets.ModelViewSet):
  queryset=RentAdvertisement.objects.all()
  serializer_class=RentAdvertisementSerializer
  filter_backends=[filters.SearchFilter,RentAdvertisementOwner]
  search_fields = ['category__name']

  def get_queryset(self):
    queryset = super().get_queryset()
    user = self.request.user
    owner_id = self.request.query_params.get('owner_id')

    if user.is_staff:
      return queryset
    elif owner_id:
      return  queryset.filter(owner=owner_id)
    else:  
      return queryset.filter(is_approved=True)

class RentRequestSpecificAdvertisement(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    requester_id=request.query_params.get('requester_id')
    owner_id = request.query_params.get('owner_id')
    if requester_id:
      return query_set.filter(requester=requester_id)
    elif owner_id:
      return query_set.filter(advertisement__owner_id=owner_id)
    return query_set
   
class RentRequestViewSet(viewsets.ModelViewSet):
   
  queryset=RentRequest.objects.all()
  serializer_class=RentRequestSerializer
  filter_backends=[RentRequestSpecificAdvertisement]
  permission_classes = [IsAuthenticated, IsOwnerOfAdvertisement] 

  def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOfAdvertisement()]
        return [IsAuthenticated()]

  def perform_update(self, serializer):
    rent_request = self.get_object()
    advertisement = rent_request.advertisement

    if self.request.user != advertisement.owner:
        raise PermissionDenied("You do not have permission to perform this action.")

    is_accepted = serializer.validated_data.get('is_accepted', rent_request.is_accepted)
    rent_request.is_accepted = is_accepted

    if advertisement.request_accepted:
        rent_request.is_accepted = False
        advertisement.request_accepted = False
    else:
        rent_request.is_accepted = True
        advertisement.request_accepted = True

    rent_request.save()
    advertisement.save()


class FavouriteSpecificAdvertisement(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    user_id=request.query_params.get('user_id')
    if user_id:
      return query_set.filter(user=user_id)
    return query_set
         
class FavouriteViewSet(viewsets.ModelViewSet):
  permission_classes=[IsAuthenticated]
  queryset=Favourite.objects.all()
  serializer_class=FavouriteSerializer
  filter_backends=[FavouriteSpecificAdvertisement]


class ReviewForSpecificAdvertisement(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    advertisement_id=request.query_params.get('advertisement_id')
    if advertisement_id:
      return query_set.filter(advertisement=advertisement_id)
    return query_set

class ReviewViewSet(viewsets.ModelViewSet):
  # permission_classes=[IsAuthenticated]
  queryset=Review.objects.all()
  serializer_class=ReviewSerializer
  filter_backends=[ReviewForSpecificAdvertisement]
