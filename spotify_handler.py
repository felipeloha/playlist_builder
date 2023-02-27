import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def spotify():
    config = configparser.ConfigParser()
    config.read("config.ini")

    client_id = config['Spotify']['client_id']
    client_secret = config['Spotify']['client_secret']
    #Authentication - without user
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_song(spotipy, search):
    result = spotipy.search(q=search, type="track")
    if not result['tracks']['items']:
        return None
    track = result['tracks']['items'][0]
    artists = ' '.join(str(artist['name']) for artist in track['artists'])
    return artists + " " + track['name']


