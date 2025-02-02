from rest_framework.permissions import BasePermission

# Custom permission to allow only the user assigned to a task to access it.
# It checks if the `assigned_to` field of the object matches the requesting user.
class IsTaskAssignee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user

# Custom permission to restrict access to admin users only.
# Checks if the authenticated user has `is_staff=True`.
class IsAdmin(BasePermission):
    """
    Custom permission to only allow admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
