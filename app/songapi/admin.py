from django.contrib import admin
from .models import SongApiSettings, Playlist, PlaylistSong

admin.site.register(SongApiSettings)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)