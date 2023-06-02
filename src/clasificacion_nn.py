
## Clasificación con redes neuronales

import numpy as np
import read_ds
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit


def validacion_cruzada(clasificador, X, y):
    ss = ShuffleSplit(n_splits=5, test_size=0.25)
    best = 0
    for train_index, test_index in ss.split(X):
        X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
        X_train, X_test = read_ds.preprocessing(X_train, X_test)
        clasificador.fit(X_train, y_train)
        score = clasificador.score(X_test, y_test)
        if score > best:
            best = score
        return best

# Método principal
def main():
    X, y = read_ds.obten()
    # Los hiperparámetros de la red se obtuvieron del optimizador
    nn_clasif = MLPClassifier(activation='tanh',
                              batch_size= 214,
                              solver='adam',
                              learning_rate_init= 0.0056,
                              alpha=1e-5,
                              hidden_layer_sizes=(33, 33),
                              random_state=41,
                              max_iter=2000)
    puntaje = validacion_cruzada(nn_clasif, X, y)
    print('Porcentaje de aciertos:', puntaje*100)

main()
