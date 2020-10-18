import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt
from fonctions_utiles import assign_rank, score_rank, add_noise_mvp
from lin_reg import linear_regression

doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'

df = pd.read_csv(doss + 'df.csv')
df = df.set_index(['Player'])

df_scaled = fonctions_utiles.normalize_by_year(df)
df_scaled = df_scaled.dropna(subset=['PER'])

def reg_lin_year_noise(df_scaled, alpha, num_iters, year):
    """
        Prédit le score avec la méthode de la régression linéaire avec du
        bruit pour les joueurs de l'année year.
        Entrainé sur toutes les autres années.
        alpha le learning rate pour la régression.
        num_iters le nombre d'itérations de descente de gradient.
    """
    test = df_scaled[df_scaled['Year'] == year]
    train = df_scaled[df_scaled['Year'] != year]
    Y_train = train['score MVP']
    Y_test = test['score MVP']
    train_imp = train[['PTS','BPM','VORP','PER','OWS','WS','TEAM_CONF_RANK']]   
    test_imp = test[['PTS','BPM','VORP','PER','OWS','WS','TEAM_CONF_RANK']]
    train_noise, Y_train_noise = add_noise_mvp(train_imp, Y_train)
    theta, cost = linear_regression(train_noise, Y_train_noise, alpha, num_iters)
    one_column = np.ones((test_imp.shape[0],1))
    test_bis = np.concatenate((one_column, test_imp), axis = 1)
    y_pred = np.dot(test_bis,np.transpose(theta)) 
    res = test_imp
    res ['score MVP'] = Y_test
    res ['pred']= y_pred
    return pd.DataFrame(res)

