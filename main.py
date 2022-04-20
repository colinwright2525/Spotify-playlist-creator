
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = '9a2c99e4311a42668443e306aab47f3f'
SPOTIPY_CLIENT_SECRET = '746408a173234000931a255abc063d79'
SPOTIPY_REDIRECT_URI = 'http://example.com'

date = input('Which year would you want to travel to? Type the date in this format YYYY-MM-DD:')
year = date.split('-')[0]
url = f'https://www.billboard.com/charts/hot-100/{date}/'

response = requests.get(url)
songs = response.text

soup = BeautifulSoup(songs, 'html.parser')
song_titles = soup.select(selector='body div main div div div div div div div ul li ul li h3')
song_titles_text = [title.getText().strip() for title in song_titles]

scope = 'playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret= SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))

user_id = sp.current_user()['id']
song_uris = []
for song in song_titles_text:
    try:
        result = sp.search(q=song)['tracks']['items'][0]['uri']
    except:
        print('This song doesn\'t exist in Spotify. Skipped')
    else:
        song_uris.append(result)


create_playlist = sp.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False)
playlist_uri = create_playlist['uri']

add_tracks = sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_uri, tracks=song_uris, position=None)


