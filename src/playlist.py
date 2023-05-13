class Playlist():
    n_playlist = 0
    def __init__(self, name, tracks):
        self.id = Playlist.n_playlist
        Playlist.n_playlist += 1
        self.name = name
        self.tracks = tracks
