
## Clasificación con redes neuronales

import numpy as np
import read_ds
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

# Método principal
def main():
    X, y = read_ds.obten()
    nn_clasif = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1, max_iter=2000)
    puntaje = np.mean(cross_val_score(nn_clasif, X, y, cv=5))
    print("Porcentaje de aciertos:",puntaje*100)

main()
