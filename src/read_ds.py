
## Este script se usará para leer y transformar el conjunto de datos

import numpy as np
from df_to_class import read_playlist
from sklearn import preprocessing

## Selecciona solo los atributos que aparecen en la lista de columnas
# @param columnas lista de nombres de columnas
# @param cancion objeto track
# @return una lista con los atributos seleccionados de esa canción
def proyeccion_unitaria(columnas, cancion, dict_artist):
    # se hará una combinación lineal de algunas variables: interestingness = loudness+tempo+(energy*100)+(danceability*100)+(acousticness*100)
    proyeccion = columnas.copy()
    interest = 0
    if 'loudness' in columnas:
        interest += cancion.features['loudness']
        proyeccion.remove('loudness')
    if 'tempo' in columnas:
        interest += cancion.features['tempo']
        proyeccion.remove('tempo')
    if 'energy' in columnas:
        interest += cancion.features['energy']*100
        proyeccion.remove('energy')
    if 'danceability' in columnas:
        interest += cancion.features['danceability']*100
        proyeccion.remove('danceability')
    if 'acousticness' in columnas:
        interest += cancion.features['acousticness']*100
        proyeccion.remove('acousticness')
    lista = []
    id_artista = dict_artist.get(cancion.artist_name)
    lista.append(id_artista) # supongo que siempre se elige el artista
    for c in proyeccion:
        lista.append(cancion.features[c])
    lista.append(interest)
    return lista

## Obtiene un diccionario de artistas. Mapea el nombre de un artista con un número.
def get_dict_artist(playlists):
    dict = {}
    indice = 1
    for pl in playlists:
        for song in pl.tracks:
            if not (song.artist_name in dict.keys()):
                dict[song.artist_name] = float(indice)
                indice += 1
    return dict

## recibe una lista de playlists y devuelve dos arreglos, X y y.
def transforma_playlist(cs, playlists):
    X_list = []
    y_list = []
    dict_art = get_dict_artist(playlists)
    for i in range(len(playlists)):
        pl = playlists[i]
        for song in pl.tracks:
            X_list.append(proyeccion_unitaria(cs, song, dict_art))
            y_list.append(pl.id)
    return (np.array(X_list), np.array(y_list))


## Reescala el conjunto de datos X.
def reescala(X):
    scaler = preprocessing.StandardScaler().fit(X)
    return scaler.transform(X)

## Lee y obtiene el conjunto de datos procesado
def obten():
    proy = ['danceability', 'energy', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms',
            'popularity_track', 'popularity_album', 'popularity_artist']
    playlist_set = read_playlist('dataset/mpd.slice.0-999-features-v2.json')
    X, y = transforma_playlist(proy, playlist_set)
    X2 = reescala(X)
    return (X2, y)