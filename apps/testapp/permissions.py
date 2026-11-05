from rest_framework.permissions import BasePermission
from .models import CustomUser

class IsModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role in [CustomUser.Role.MODERATOR, CustomUser.Role.ADMIN]

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        elif request.user.role not in [CustomUser.Role.ADMIN]:
            return False
        
        return request.user.role == CustomUser.Role.ADMIN

class IsUserOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role == CustomUser.Role.USER