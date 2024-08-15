from typing import Any
from django.contrib import admin
from .models import User,UserBankAccount
# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display=['username','first_name','last_name','email','role']
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


class UserBankAccountAdmin(admin.ModelAdmin):
    list_display=['account_no','full_name','balance']

    def full_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


admin.site.register(UserBankAccount,UserBankAccountAdmin)