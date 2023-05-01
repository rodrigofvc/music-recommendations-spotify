import json
import pandas as pd
import numpy as np
import requests

# Replace here the TOKEN from api
TOKEN = 'BQAWecaSq0plGUufi4FK5bKqXvM_EzsO3UfU0ByLX-CqL3MMwJqTnYMtSZxFX2VmUv5lbo91JBbJGvT2eLvrhI0-xfmMV3ur-iX1To_PjsKHZj9GziBs'
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
    for i in range(d.shape[0]):
        playlist = d[i]
        for j in range(len(playlist[7])):
            track = playlist[7][j]
            features = get_features_track(track['track_uri'])
            d[i][7][j]['features'] = features
    new_df = pd.DataFrame(d, columns=columns)
    new_path = path_data.replace('.json', '-features.json')
    new_df.to_json(new_path, orient='split')

# Get the features from  mpd.slice.0-999.json file and save it as mpd.slice.0-999-features.json
get_features_dataset('mpd.slice.0-999.json')
