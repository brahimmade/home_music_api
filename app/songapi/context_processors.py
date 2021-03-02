from .models import SongApiSettings

def settings(request):
    return {'settings': SongApiSettings.load()}