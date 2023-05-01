class Track():

    """
    features:
        danceability
        energy
        key
        loudness
        mode
        speechiness
        acousticness
        instrumentalness
        liveness
        valence
        tempo
        type
        id
        uri
        track_href
        analysis_url
        duration_ms
        time_signature
    """
    def __init__(self, name, artist_name, features):
        self.name = name
        self.artist_name = artist_name
        self.features = features

    def __str__(self):
        d = {'name': self.name, 'artist_name': self.artist_name, 'features': self.features}
        return str(d)
