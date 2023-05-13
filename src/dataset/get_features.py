import json
import pandas as pd
import numpy as np
import requests

# Replace here the TOKEN from api
TOKEN = ''
headers = {'Authorization': 'Bearer  ' + TOKEN}

# Make a request for features of track
def get_features_track(track_id):
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

# Get the features from datasets list and save it as mpd.slice.0-999-features.json
# 34 1000-1999
# 29 2000-2999
# 37 3000-3999
# 32 4000-4999
# 38 5000-5999
get_features_dataset('mpd.slice.1000-1999.json')
get_features_dataset('mpd.slice.2000-2999.json')
get_features_dataset('mpd.slice.3000-3999.json')
get_features_dataset('mpd.slice.4000-4999.json')
get_features_dataset('mpd.slice.5000-5999.json')
