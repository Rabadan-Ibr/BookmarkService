from rest_framework import serializers

from apps.bookmarks.models import Bookmark, Collection


class BookmarkLinkSerializer(serializers.Serializer):
    """
    Сериализатор для получения ссылки для создания закладки
    """

    url = serializers.URLField()


class BookmarkListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения закладок в списке
    """

    class Meta:
        model = Bookmark
        fields = ('id', 'title', 'image', 'url')


class BookmarkCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания закладки
    """

    class Meta:
        model = Bookmark
        fields = (
            'id',
            'title',
            'description',
            'url',
            'type',
            'image',
        )


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отображения закладки
    """

    class Meta:
        model = Bookmark
        fields = (
            'id',
            'title',
            'description',
            'pub_date',
            'modify_date',
            'url',
            'type',
            'image',
        )
        read_only_fields = ('pub_date', 'modify_date')


class CollectionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и изменения коллекции
    """

    class Meta:
        model = Collection
        fields = ('id', 'title', 'description')


class CollectionListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения коллекций в списке
    """

    class Meta:
        model = Collection
        fields = ('id', 'title', 'pub_date')


class CollectionDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отображения коллекции
    """

    bookmarks = BookmarkSerializer(many=True)

    class Meta:
        model = Collection
        fields = (
            'id',
            'title',
            'description',
            'pub_date',
            'modify_date',
            'bookmarks',
        )
        read_only_fields = ('pub_date', 'modify_date')


class AddBookmarkToCollectionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления закладки в коллекцию
    """

    bookmark = serializers.PrimaryKeyRelatedField(
        queryset=Bookmark.objects, source='bookmarks'
    )

    class Meta:
        model = Collection
        fields = ('bookmark',)

    def update(self, instance, validated_data):
        bookmark = validated_data['bookmarks']
        instance.bookmarks.add(bookmark)
        return instance
