import json
import pandas as pd
import numpy as np

from playlist import *
from track import *

def read_playlist(path_data):
    re = json.load(open(path_data))
    columns = ['name', 'collaborative', 'pid', 'modified_at', 'num_tracks', 'num_albums', 'num_followers', 'tracks', 'num_edits', 'duration_ms', 'num_artists', 'description']
    df = pd.DataFrame(re['data'], columns=columns)
    d = df.to_numpy()
    playlist_list = []
    for i in range(d.shape[0]):
        playlist = d[i]
        name_playlist = playlist[0]
        tracks = playlist[7]
        tracks_list = []
        for track in tracks:
            name = track['track_name']
            artist_name = track['artist_name']
            features = track['features']
            t = Track(name, artist_name, features)
            if track['track_uri'] != features['uri'] :
                raise()
            tracks_list.append(t)
        p = Playlist(i, name_playlist, tracks_list)
        playlist_list.append(p)
    return playlist_list

read_playlist('dataset/mpd.slice.0-999-features.json')
