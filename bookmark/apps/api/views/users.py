from djoser.serializers import UserCreateSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.api.serializers.users import UserSerializer
from apps.users.models import User


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects

    action_serializers = {
        'create': UserCreateSerializer,
        'me': UserSerializer,
    }

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        serializer = self.action_serializers.get(self.action, None)
        if serializer is None:
            raise AttributeError(
                f'Not found serializer for action: {self.action}'
            )
        return serializer

    def get_queryset(self):
        return self.queryset.filter(pk=self.request.user.pk)

    @extend_schema(
        description='Получение данных пользователя',
        methods=('GET',),
        operation_id='User get data',
    )
    @extend_schema(
        description='Изменение данных пользователя',
        methods=('PATCH',),
        operation_id='User change data',
    )
    @action(('get', 'patch'), detail=False)
    def me(self, request, *args, **kwargs):
        """ Выдача данных пользователя и изменение данных """
        user = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
