from df_to_class import read_playlist


if __name__ == '__main__':
    # 39 playlist
    playlist_set = read_playlist('dataset/mpd.slice.0-999-features.json')
    # Print all tracks in the first playlist
    first_playlist = playlist_set[0]
    for track in first_playlist.tracks:
        print (track)
    #for pl in playlist_set:
    #    print('id', pl.id, 'name', pl.name)
