from django.shortcuts import render
from rest_framework import viewsets,filters,status
from .models import RentAdvertisement,RentRequest,Favourite,Review
from account.models import UserBankAccount
from .serializers import RentAdvertisementSerializer,RentRequestSerializer,FavouriteSerializer,ReviewSerializer

from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from django.core.exceptions import ValidationError
from django.db.models import Q 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOfAdvertisement
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404

# Create your views here.

class RentAdvertisementOwner(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    owner_id=request.query_params.get('owner_id')
    if owner_id :
      return query_set.filter(owner=owner_id)
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
  
    if owner_id:
      return queryset.filter(owner=owner_id)
    elif user.is_staff:
      return  queryset
    else:  
      return queryset.filter(is_approved=True)


  def update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_approved_value = request.data.get('is_approved')
    
        # Check if the user is an admin
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
  
        if instance.is_approved:
            instance.is_approved = False
            instance.save()
        else:
            instance.is_approved = True
            instance.save()

        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

  def destroy(self, request, *args, **kwargs):
        try:
            advertisement = get_object_or_404(RentAdvertisement, pk=kwargs['pk'])
            print(advertisement)
            self.perform_destroy(advertisement)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RentAdvertisement.DoesNotExist:
            return Response({'error': 'Advertisement not found'}, status=status.HTTP_404_NOT_FOUND)

  def perform_destroy(self, instance):
        instance.delete()




class RentRequestSpecificAdvertisement(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
   
    requester_id=request.query_params.get('requester_id')
    owner_id = request.query_params.get('owner_id')
    advertisement_id=request.query_params.get('advertisement_id')
    
    if requester_id:
      return query_set.filter(requester=requester_id)
    elif owner_id:
      return query_set.filter(advertisement__owner_id=owner_id)
    elif advertisement_id:
      return query_set.filter(advertisement=advertisement_id)
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

  def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if the user has a bank account and sufficient balance
        advertisement = serializer.validated_data.get('advertisement')
        user_account = UserBankAccount.objects.filter(user_id=request.user.id).first()

        if user_account is None:
            return Response({"error": "User does not have a bank account."}, status=status.HTTP_400_BAD_REQUEST)

        if user_account.balance < advertisement.price:
            return Response({"error": "Insufficient balance to make this rent request."}, status=status.HTTP_400_BAD_REQUEST)

      
        self.perform_create(serializer)
        
       
        user_account.balance -= advertisement.price
        user_account.save()

        advertisement.request_accepted = True
        advertisement.save()

        rent_request = serializer.instance
        rent_request.is_accepted = True
        rent_request.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

  def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
        

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

  def destroy(self, request, *args, **kwargs):
    rent_request = self.get_object()
    advertisement = rent_request.advertisement
    
    response = super().destroy(request, *args, **kwargs)
        
    if advertisement.request_accepted:
      advertisement.request_accepted = False
      advertisement.save()

    return response


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

  def perform_create(self,serializer):
    advertisement_id = serializer.validated_data['advertisement'].id
    user = self.request.user

    if not RentRequest.objects.filter(advertisement_id=advertisement_id, requester=user, is_accepted=True).exists():
       raise PermissionDenied("You must have send rent request  an accepted rent request for this advertisement before you can leave a review.")
    serializer.save(reviewer=user)
