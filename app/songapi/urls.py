from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'song', SongViewSet)
router.register(r'album', AlbumViewSet)
router.register(r'artist', ArtistViewSet)
router.register(r'playlist', PlaylistViewSet)
router.register(r'playlistsong', PlaylistSongViewSet)

urlpatterns = [
 path('', include(router.urls)),
 path('refresh_songs/', refresh_songs, name='refresh_songs'),
 path('get_user_settings/', get_user_settings, name='get_user_settings'),
 path('set_user_settings/', set_user_settings, name='set_user_settings'),
 path('get_refresh_status/', get_refresh_status, name='get_refresh_status'),
 path('set_refresh_status/', set_refresh_status, name='set_refresh_status'),
]
