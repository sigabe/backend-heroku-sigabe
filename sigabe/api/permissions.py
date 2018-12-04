from rest_framework import permissions


class WithinCicle(permissions.BasePermission):
    message = 'Credential false'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all()
