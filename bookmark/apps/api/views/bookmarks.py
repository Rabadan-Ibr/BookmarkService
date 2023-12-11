import requests.exceptions
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.api.serializers.bookmarks import BookmarkLinkSerializer, \
    BookmarkSerializer, BookmarkListSerializer, \
    CollectionCreateUpdateSerializer, CollectionDetailSerializer, \
    CollectionListSerializer, AddBookmarkToCollectionSerializer
from apps.bookmarks.models import Bookmark, Collection
from apps.bookmarks.services import OpenGraphParse


class BookmarkViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Вьюсет для закладок.
    """
    queryset = Bookmark.objects

    action_serializers = {
        'create': BookmarkLinkSerializer,
        'retrieve': BookmarkSerializer,
        'list': BookmarkListSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

    def get_serializer_class(self):
        serializer = self.action_serializers.get(self.action, None)
        if serializer is None:
            raise AttributeError(
                f'Not found serializer for action: {self.action}'
            )
        return serializer

    @extend_schema(
        description='Создание закладки',
        operation_id='Create bookmark',
        responses=BookmarkSerializer,
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # По хорошему отправку запроса и парсинг лучше добавить в очередь задач
        # Но не это не в рамках данного тестового
        try:
            graph = OpenGraphParse(serializer.data['url'])
        except OpenGraphParse.PageRetrieveException:
            return Response(
                {'error': "Can't get the page from the link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = graph.get_data
        type_page = data.get('type', None)
        if type_page and type_page not in Bookmark.support_types():
            data.pop('type')

        serializer = BookmarkSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для коллекций.
    """
    queryset = Collection.objects

    action_serializers = {
        'create': CollectionCreateUpdateSerializer,
        'retrieve': CollectionDetailSerializer,
        'list': CollectionListSerializer,
        'update': CollectionCreateUpdateSerializer,
        'partial_update': CollectionCreateUpdateSerializer,
        'add_bookmark': AddBookmarkToCollectionSerializer,
    }

    def get_serializer_class(self):
        serializer = self.action_serializers.get(self.action, None)
        if serializer is None:
            raise AttributeError(
                f'Not found serializer for action: {self.action}'
            )
        return serializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        description='Добавление закладки в коллекцию',
        operation_id='Add bookmark',
        responses=CollectionDetailSerializer,
    )
    @action(methods=('POST',), detail=True)
    def add_bookmark(self, request, pk):
        """
        Добавление закладки в коллекцию
        """
        collection = self.get_object()
        serializer = self.get_serializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = CollectionDetailSerializer(collection)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        description='Удаление закладки из коллекции',
        operation_id='Remove bookmark',
    )
    @action(
        methods=('DELETE',),
        detail=True,
        url_path='remove_bookmark/(?P<bm_pk>[^/.]+)',
    )
    def remove_bookmark(self, request, pk, bm_pk):
        """
        Удаление закладки из коллекции
        """
        collection = self.get_object()
        bookmark = get_object_or_404(Bookmark, pk=bm_pk)
        collection.bookmarks.remove(bookmark)
        return Response(status=status.HTTP_204_NO_CONTENT)
