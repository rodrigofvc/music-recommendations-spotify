
import numpy as np
from df_to_class import read_playlist
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold

## Selecciona solo los atributos que aparecen en la lista de columnas
# @param columnas lista de nombres de columnas
# @param cancion objeto track
# @return una lista con los atributos seleccionados de esa canción
def proyeccion_unitaria(columnas, cancion):
    lista = []
    hc_an = hash(cancion.artist_name) % 10000
    lista.append(hc_an) # supongo que siempre se elige el artista
    for c in columnas:
        objeto = cancion.features[c]
        # para operar con puros números, se transformarán los strings a números
        if isinstance(objeto, str):
            hc = hash(objeto) % 10000
            lista.append(hc)
        else:
            lista.append(objeto)
    return lista

# recibe una lista de playlists y devuelve dos arreglos, X y y.
def transforma_playlist(cs, playlists):
    X_list = []
    y_list = []
    for i in range(len(playlists)):
        pl = playlists[i]
        for song in pl.tracks:
            X_list.append(proyeccion_unitaria(cs, song))
            y_list.append(pl.id)
    return (np.array(X_list), np.array(y_list))

# Se reescalan los datos
def reescalado(X):
    X2 = np.ones(X.shape)
    for c in range(X.shape[1]):
        columna = X[:,c]
        xmax = columna.max()
        xmin = columna.min()
        for f in range(X.shape[0]):
            X2[f][c] = (X[f][c] - xmin)/(xmax - xmin)
    return X2

def aciertos(y_pred, y_real):
    ac = 0
    for i in range(y_pred.shape[0]):
        if y_pred[i] == y_real[i]:
            ac += 1
    return ac/y_pred.shape[0]

# devuelve los aciertos promedio
def evalua(ns, X, y, clasificador):
    skf = StratifiedKFold(n_splits=ns)
    razon_aciertos = 0
    for train_index, test_index in skf.split(X, y):
        X_train = X[train_index]
        y_train = y[train_index]
        X_test = X[test_index]
        y_test = y[test_index]
        clasificador.fit(X_train, y_train)
        y_pred = clasificador.predict(X_test)
        razon_aciertos += aciertos(y_pred, y_test)
    return razon_aciertos/ns

# Método principal
def main():
    proy = ['danceability', 'energy', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    playlist_set = read_playlist('dataset/mpd.slice.0-999-features.json')
    X, y = transforma_playlist(proy, playlist_set)
    X = reescalado(X)
    nn_clasif = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    razon_aciertos = evalua(6, X, y, nn_clasif)
    print('Porcentaje de aciertos:', razon_aciertos*100)

main()
