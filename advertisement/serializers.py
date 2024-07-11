from rest_framework import serializers
from .models import RentAdvertisement,RentRequest,Favourite,Review

class RentAdvertisementSerializer(serializers.ModelSerializer):
  # category=serializers.StringRelatedField(many=False)
  class Meta:
    model=RentAdvertisement
    fields='__all__'


class RentRequestSerializer(serializers.ModelSerializer):
  
  class Meta:
    model=RentRequest
    fields='__all__'


class FavouriteSerializer(serializers.ModelSerializer):

  class Meta:
    model=Favourite
    fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
  
  class Meta:
    model=Review
    fields='__all__'
