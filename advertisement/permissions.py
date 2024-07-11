from rest_framework.permissions import BasePermission

class IsOwnerOfAdvertisement(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.advertisement.owner == request.user
