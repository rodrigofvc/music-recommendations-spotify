from df_to_class import read_playlist


if __name__ == '__main__':
    # 39 playlist
    playlist_set = read_playlist('dataset/mpd.slice.0-999-features.json')
    for track in playlist_set[0].tracks:
        print (track)
    
