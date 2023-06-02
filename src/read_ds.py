
## Este script se usará para leer y transformar el conjunto de datos

import numpy as np
from df_to_class import read_playlist
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

danceability_index = 0 
energy_index = 1
key_index = 2
loudness_index = 3
mode_index =  4
speechiness_index = 5
acousticness_index = 6 
instrumentalness_index = 7  
liveness_index =  8
valence_index =  9
tempo_index = 10 
duration_ms_index = 11 
time_signature_index = 12
popularity_track_index = 13 
popularity_album_index =  14
popularity_artist_index = 15

## Selecciona solo los atributos que aparecen en la lista de columnas
# @param columnas lista de nombres de columnas
# @param cancion objeto track
# @return una lista con los atributos seleccionados de esa canción
def proyeccion_unitaria(columnas, cancion):
    lista = []
    for c in columnas:
        lista.append(cancion.features[c])
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
    for pl in playlists:
        for song in pl.tracks:
            X_list.append(proyeccion_unitaria(cs, song))
            y_list.append(pl.id)
    return (np.array(X_list), np.array(y_list))

## Reescala el conjunto de datos X.
def reescala(X):
    scaler = StandardScaler().fit(X)
    return scaler.transform(X)

def ms_a_minutos(X_in):
    X_in[:,duration_ms_index] = (X_in[:,duration_ms_index] / 1000) / 60

## Obtiene una combinación lineal de las popularidades.
# @return la concatenación de X_in con la nueva columna de popularidad
def popularidad(X_in):
    track = X_in[:,popularity_track_index]
    artist = X_in[:,popularity_artist_index]
    album = X_in[:,popularity_album_index]
    popularity = np.zeros((track.shape))
    popularity = 3*track + 2*artist + album
    popularity_column = popularity[:,np.newaxis]
    return np.concatenate([X_in, popularity_column], axis=1)

def calcula_popularidad_index(X_in):
    I = np.zeros((X_in.shape[0], 1))
    I = 3*X_in[:, popularity_track_index] + 2*X_in[:, popularity_artist_index] + X_in[:, popularity_album_index]
    X_in = np.concatenate((X_in, I.reshape(-1,1)), axis=1)
    return X_in

def normaliza(X_in):
    # Columnas que si se deben normalizar
    indexes = [c for c in range(0,16) if c != loudness_index and c != duration_ms_index]
    # Entrena y transforma usando solo las columnas
    transformer = StandardScaler().fit(X_in[:, indexes])
    XN = transformer.transform(X_in[:, indexes])
    # Concatenar las columnas transformadas con las 2 restantes
    XZ = np.concatenate((XN[:, [0,1,2]], X_in[:,loudness_index].reshape(-1,1)), axis=1)
    XZ = np.concatenate((XZ[:,:], XN[:,[3,4,5,6,7,8,9]]), axis=1)
    XZ = np.concatenate((XZ[:,:], X_in[:,duration_ms_index].reshape(-1,1)), axis=1)
    XZ = np.concatenate((XZ[:,:], XN[:,[10,11,12,13]]), axis=1)
    return transformer, XZ   

def interesting(X_int):
    I = np.zeros((X_int.shape[0], 1))
    I = X_int[:, loudness_index] + X_int[:, tempo_index] + (X_int[:, energy_index]) * 100 + (X_int[:, danceability_index]) * 100 + (X_int[:, acousticness_index]) * 100 
    X_int = np.concatenate((X_int, I.reshape(-1,1)), axis=1)
    return X_int

def transforma_test(transformer, X_in):
    indexes = [c for c in range(0,16) if c != loudness_index and c != duration_ms_index]
    XTT = transformer.transform(X_in[:, indexes])
    XT = np.concatenate((XTT[:, [0,1,2]], X_in[:,loudness_index].reshape(-1,1)), axis=1)
    XT = np.concatenate((XT[:,:], XTT[:,[3,4,5,6,7,8,9]]), axis=1)
    XT = np.concatenate((XT[:,:], X_in[:,duration_ms_index].reshape(-1,1)), axis=1)
    XT = np.concatenate((XT[:,:], XTT[:,[10,11,12,13]]), axis=1)
    return XT

def preprocessing(x_train, x_test):
    ms_a_minutos(x_test)
    ms_a_minutos(x_train)
    transformer, x_train = normaliza(x_train)
    x_train = interesting(x_train)
    x_test = transforma_test(transformer, x_test)
    x_test = interesting(x_test)
    x_train = calcula_popularidad_index(x_train)
    x_test = calcula_popularidad_index(x_test)
    return x_train, x_test

## Lee y obtiene el conjunto de datos en crudo
def obten():
    proy = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 
            'duration_ms', 'time_signature', 'popularity_track', 'popularity_album', 'popularity_artist']
    playlist_set = read_playlist('dataset/mpd.slice.0-999-features-v2.json')
    return transforma_playlist(proy, playlist_set)

## Devuelve los datos preprocesados
def obten2():
    X, y = obten()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_pp, X_test_pp = preprocessing(X_train, X_test)
    return (np.concatenate([X_train_pp, X_test_pp], axis=0), np.concatenate([y_train, y_test], axis = 0))

def main():
    X, y = obten2()
    print('X.shape', X.shape)
    print('y.shape', y.shape)


