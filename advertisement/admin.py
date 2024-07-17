from django.contrib import admin
from .models import RentAdvertisement,RentRequest,Favourite,Review
from rest_framework.response import Response
# Register your models here.

class RentAdvertisementAdmin(admin.ModelAdmin):
   list_display=['title','category','is_approved','request_accepted','bedrooms']
   def save_model(self, request,obj,form,chnage) -> None:
    
    obj.save()
    if obj.is_approved==True:
      obj.is_approved=True
    else:
      obj.is_approved=True
    obj.save()

admin.site.register(RentAdvertisement,RentAdvertisementAdmin)

class RentRequestAdmin(admin.ModelAdmin):
   list_display=['getadvertisement','requester','is_accepted']

   def getadvertisement(self,obj):
     return obj.advertisement.title
  
   def requester(self,obj):
     return obj.requester.first_name

  #  def save_model(self, request,obj,form,chnage) -> None:
    
  #   obj.save()
  #   if  obj.advertisement.request_accepted:
  #     obj.is_accepted = False
  #     obj.save()
  #     obj.advertisement.request_accepted = False
  #     obj.advertisement.save()
  #   else:
  #     obj.is_accepted = True
  #     obj.save()
  #     obj.advertisement.request_accepted = True
  #     obj.advertisement.save()

admin.site.register(RentRequest,RentRequestAdmin)
admin.site.register(Favourite)
admin.site.register(Review)
