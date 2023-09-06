from rest_framework.permissions import BasePermission


class IsOwnerOrModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object().owner or request.user.groups.filter(name='Moderator').exists()


class IsNotModerator(BasePermission):

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='Moderator').exists()

