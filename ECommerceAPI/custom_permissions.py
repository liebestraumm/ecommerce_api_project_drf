from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(request.user).exists()

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery Crew').exists()
