import requests
import json
import functions
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

# print(functions.get_spotify_recent())
# other 


scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_recently_played(limit=50)
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
    before = results['cursors']['before']

print("this is before value: " +str(before))

# print(json.dumps(results,indent=4))
try:
    results = sp.current_user_recently_played(before=before)
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
except Exception as e:
    print(e)
# results = sp.current_user_recently_played(limit=50,after=150)
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])
