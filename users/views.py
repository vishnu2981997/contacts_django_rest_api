from rest_framework import permissions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all().order_by('id')
        else:
            return User.objects.none()

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        return self.order(recent_users)

    @action(detail=False, permission_classes=[permissions.IsAdminUser])
    def active_users(self, request):
        """
        Returns active users
        """
        active_users = User.objects.filter(is_active=True).order_by("id")

        return self.order(active_users)

    def order(self, data):
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(data, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
