from rest_framework import permissions 

class IsOwnerOrReadOnly(permissions.BasePermission): 
    """Custom permissions that can be set at the object level."""

    def has_object_permission(self, request, view, obj): 
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
