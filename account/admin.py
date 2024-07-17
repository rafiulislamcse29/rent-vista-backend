from typing import Any
from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display=['first_name','last_name','username','email','role']
  def save_model(self, request, obj, form, change):
        if obj.role == 'admin':
            obj.is_superuser = True
            obj.is_staff = True
            obj.role == 'admin'
        else:
            obj.is_superuser = False
            obj.is_staff = False
            obj.role == 'user'
        obj.save()
      

admin.site.register(User,UserAdmin)