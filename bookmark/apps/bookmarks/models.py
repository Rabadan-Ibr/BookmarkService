from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserCreatedBase(models.Model):
    """
    Базовая модель
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название', max_length=300)
    description = models.TextField('Описание')
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)
    modify_date = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Bookmark(UserCreatedBase):
    """
    Модель закладки.
    """

    WEBSITE = 'website'
    BOOK = 'book'
    ARTICLE = 'article'
    MUSIC = 'music'
    VIDEO = 'video'

    TYPE_CHOICES = {
        WEBSITE: 'Website',
        BOOK: 'Book',
        ARTICLE: 'Article',
        MUSIC: 'Music',
        VIDEO: 'Video',
    }

    url = models.CharField('Link', max_length=300)
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default=WEBSITE
    )
    image = models.CharField(
        'Preview image', max_length=300, blank=True, null=True
    )

    class Meta(UserCreatedBase.Meta):
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'
        default_related_name = 'bookmarks'

    @classmethod
    def support_types(cls):
        return (_ for _ in cls.TYPE_CHOICES.keys())


class Collection(UserCreatedBase):
    """
    Модель коллекции
    """
    bookmarks = models.ManyToManyField(
        Bookmark,
        verbose_name='Bookmarks',
        related_name='collections',
    )

    class Meta(UserCreatedBase.Meta):
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
        default_related_name = 'collections'
