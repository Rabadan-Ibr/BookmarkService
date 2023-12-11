from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework.routers import SimpleRouter

from apps.api.views.bookmarks import BookmarkViewSet, CollectionViewSet
from apps.api.views.users import UserViewSet

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet)
v1_router.register('bookmarks', BookmarkViewSet)
v1_router.register('collections', CollectionViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'v1/doc/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger'
    ),
]