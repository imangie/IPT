from rest_framework.permissions import BasePermission


class IsTaskAssignee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user

class IsAdmin(BasePermission):
    """
    Custom permission to only allow admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # or check for admin role