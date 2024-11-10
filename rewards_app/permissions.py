from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has admin role
        return request.user.is_authenticated and request.user.role == 'admin'
