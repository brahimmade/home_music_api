from distutils.util import strtobool
from rest_framework import viewsets 

from rest_framework.decorators import api_view, permission_classes #for no model 
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework import filters

from .serializers import SongSerializer, AlbumSerializer, ArtistSerializer, PlaylistSerializer, PlaylistSongSerializer

from .models import Song, Album, Artist, Playlist, PlaylistSong, SongApiUserSettings, SongApiSourceFiles

from .extra_methods import SongProcessing

class AlbumViewSet(viewsets.ModelViewSet): 
	permission_classes = (IsAuthenticated,)
	'''
	model based:
	define queryset
	specify serializer to be used
	set fields to allow automated search queries, 
	note:
	foreign key uses double underscore notation	(double underscore for search into relatred table)
	'''
	queryset = Album.objects.all()  
	serializer_class = AlbumSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['name'] 

class ArtistViewSet(viewsets.ModelViewSet): 
	permission_classes = (IsAuthenticated,)

	queryset = Artist.objects.all()  
	serializer_class = ArtistSerializer 
	filter_backends = [filters.SearchFilter]
	search_fields = ['name'] 

class SongViewSet(viewsets.ModelViewSet): 
	permission_classes = (IsAuthenticated,)

	queryset = Song.objects.all()  
	serializer_class = SongSerializer 
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'album__name', 'artist__name']  

class PlaylistViewSet(viewsets.ModelViewSet):  
	permission_classes = (IsAuthenticated,)

	queryset = Playlist.objects.all()  
	serializer_class = PlaylistSerializer 
	filter_backends = [filters.SearchFilter]
	search_fields = ['name'] 

class PlaylistSongViewSet(viewsets.ModelViewSet):  
	permission_classes = (IsAuthenticated,)

	queryset = PlaylistSong.objects.all()  
	serializer_class = PlaylistSongSerializer 
	filter_backends = [filters.SearchFilter]
	search_fields = ['playlist__id', 'song__id', 'playlist__name', 'song__title', 'created_at'] 

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def refresh_songs(request):
	'''
	non-model based view to add / remove songs from database when they are added or removed from file system
	'''
	if request.method == 'GET':
		objSongs = SongProcessing()
		returnData = objSongs.RefreshSongs()
		return Response(returnData)

	return Response({"message": "GET - refresh_songs, no POST or DELETE"})

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_settings(request):
	
	if request.method == 'GET':
		obj = SongApiUserSettings.objects.all().values()
		returnData = obj
		return Response(returnData)

	return Response({"message": "GET - get_user_settings, no POST or DELETE"})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def set_user_settings(request):
	
	if request.method == 'POST':
		objSettings = SongApiUserSettings.objects.first()
		objSettings.source_ip = request.POST.get('source_ip')
		objSettings.source_script_path = request.POST.get('source_script_path')
		objSettings.save()
		returnData = SongApiUserSettings.objects.all().values()
		return Response(returnData)

	return Response({"message": "POST - set_user_settings, no GET or DELETE"})

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_refresh_status(request):
	
	if request.method == 'GET':
		obj = SongApiSourceFiles.objects.only().values('refresh_underway')
		return Response(obj)

	return Response({"message": "GET - get_refresh_status, no POST or DELETE"})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def set_refresh_status(request):
	
	if request.method == 'POST':
		postVal = request.POST.get('refresh')
		newVal = strtobool(postVal)
		convertedVal = bool(newVal)
		obj = SongApiSourceFiles.objects.first()
		obj.refresh_underway = convertedVal
		obj.save()
		returnData = SongApiSourceFiles.objects.all().values()
		return Response(returnData)

	return Response({"message": "POST - set_user_settings, no GET or DELETE"})
