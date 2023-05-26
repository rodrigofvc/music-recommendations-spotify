import json
import pandas as pd
import numpy as np
import requests
import time
from track import Track
from dataset.get_token import request_token

# Replace here the TOKEN from api
TOKEN = 'BQC734ElCgRRqHtYy9rRsBT3zRw8vBLdmt-FhDr7O_11nEXJwc-X5lKW8wdDGu0cGvR0rvvfwaWpVoCI1IP41lRKv1KJvXZv_eemAv_b_UgoEs1LzBE'
headers = {'Authorization': 'Bearer  ' + TOKEN}

# Make a request for features of track
def get_features_track(track_id):
    global headers
    track_id = track_id.replace('spotify:track:', '')
    get_url = 'https://api.spotify.com/v1/audio-features/' + track_id
    r = requests.get(get_url, headers=headers)
    return r.json()

# Take playlist with 200 or more tracks and download its features
def get_features_dataset(path_data):
    data = json.load(open(path_data))
    df = pd.DataFrame(data["playlists"])
    columns = df.columns
    df = df[df['num_tracks'] >= 200]
    d = df.to_numpy()
    t = d.shape[0]
    for i in range(d.shape[0]):
        playlist = d[i]
        for j in range(len(playlist[7])):
            track = playlist[7][j]
            features = get_features_track(track['track_uri'])
            d[i][7][j]['features'] = features
            print (f'dataset {path_data} - {i}|{j}  /{t}')
    new_df = pd.DataFrame(d, columns=columns)
    new_path = path_data.replace('.json', '-features.json')
    new_df.to_json(new_path, orient='split')

def get_popularity_album(id):
    global headers
    get_url = 'https://api.spotify.com/v1/albums/' + id
    r = requests.get(get_url, headers=headers)
    r = refresh_token(r, get_url)
    d = r.json()
    return d['popularity']

def get_popularity_artist(id):
    global headers
    get_url = 'https://api.spotify.com/v1/artists/' + id
    r = requests.get(get_url, headers=headers)
    r = refresh_token(r, get_url)
    d = r.json()
    if 'popularity' in d.keys():
        return d['popularity']
    return 0

def refresh_token(r, request_url):
    global headers
    if r.status_code == 401:
        TOKEN = request_token()
        headers = {'Authorization': 'Bearer  ' + TOKEN}
        return requests.get(request_url, headers=headers)
    elif r.status_code == 429:
        raise('session exceeded')
    return r

def features_popularity(tracks):
    global headers
    for d in tracks:
        d['features']['popularity_track'] = 0
        d['features']['popularity_album'] = 0
        d['features']['popularity_artist'] = 0
    get_url = 'https://api.spotify.com/v1/tracks'
    uris = [t['features']['uri'][14:] for t in tracks]
    for i in range(0, len(uris), 50):
        ids = uris[i:i+50]
        ids = ','.join(ids)
        request_url = get_url + '?ids=' + ids
        r = requests.get(request_url, headers=headers)
        r = refresh_token(r, request_url)
        d = r.json()
        print (f'{i}-{i+50} {len(uris)}')
        for d_track in d['tracks']:
            if d_track == None:
                continue

            popularity_album = 0
            popularity_track = 0
            popularity_artist = 0
            popularity_album = get_popularity_album(d_track['album']['id'])
            popularity_artist = get_popularity_artist(d_track['artists'][0]['id'])
            if 'popularity' in d_track.keys():
                popularity_track = d_track['popularity']
            uri = d_track['uri']
            track = [t for t in tracks if t['features']['uri'] == uri][0]
            track['features']['popularity_track'] = popularity_album
            track['features']['popularity_album'] = popularity_track
            track['features']['popularity_artist'] = popularity_artist
        time.sleep(55)


def get_features_popularity_dataset(path_data, index_playlist):
    global headers
    re = json.load(open(path_data))
    columns = ['name', 'collaborative', 'pid', 'modified_at', 'num_tracks', 'num_albums', 'num_followers', 'tracks', 'num_edits', 'duration_ms', 'num_artists', 'description']
    df = pd.DataFrame(re['data'], columns=columns)
    d = df.to_numpy()
    start = time.time()
    for i in range(index_playlist, d.shape[0]):
        playlist = d[i]
        name_playlist = playlist[0]
        tracks = playlist[7]
        tracks_list = []
        print (f'Playlist  {i} / {d.shape[0]}')
        features_popularity(tracks)
        for track in tracks:
            name = track['track_name']
            artist_name = track['artist_name']
            features = track['features']
            t = Track(name, artist_name, features)
            if track['track_uri'] != features['uri'] :
                raise()
            tracks_list.append(t)
        current = time.time()
        if (current-start) >= 3000:
            TOKEN = request_token()
            headers = {'Authorization': 'Bearer  ' + TOKEN}
            start = time.time()
        new_df = pd.DataFrame(d, columns=columns)
        new_df.to_json(path_data, orient='split')
        #dataset/mpd.slice.1000-1999-features-v2.json | Playlist  5 / 34 SAVED <<<<<<<<<<<
        print (f'{path_data} | Playlist  {i} / {d.shape[0]} SAVED <<<<<<<<<<< ')


# Get the features from datasets list and save it as mpd.slice.0-999-features.json
# 34 1000-1999
#get_features_dataset('mpd.slice.1000-1999.json')
# 29 2000-2999
#get_features_dataset('mpd.slice.2000-2999.json')
# 37 3000-3999
#get_features_dataset('mpd.slice.3000-3999.json')
# 32 4000-4999
#get_features_dataset('mpd.slice.4000-4999.json')
# 38 5000-5999
#get_features_dataset('mpd.slice.5000-5999.json')
#get_features_popularity_dataset('dataset/mpd.slice.0-999-features-v2.json', 0)
get_features_popularity_dataset('dataset/mpd.slice.1000-1999-features-v2.json', 6)
