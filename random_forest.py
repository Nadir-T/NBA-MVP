import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt
from fonctions_utiles import assign_rank, score_rank, add_noise_mvp, coupe

from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression


doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'
doss_res = '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Résultats/'

df = pd.read_csv(doss + 'df.csv')
df = df.set_index(['Player'])

df_scaled = fonctions_utiles.normalize_by_year(df)
df_scaled = df_scaled.dropna(subset=['PER'])



def rf_year(df_scaled, alpha, num_iters, year):
    """
        Prédit le score avec une random forest pour les joueurs de l'année year.
        Entrainé sur toutes les autres années.
    """
    test = df_scaled[df_scaled['Year'] == year]
    train = df_scaled[df_scaled['Year'] != year]
    Y_train = train['score MVP']
    Y_test = test['score MVP']
    train_imp = train[['PTS','BPM','VORP','PER','OWS','WS','TEAM_CONF_RANK']]   
    test_imp = test[['PTS','BPM','VORP','PER','OWS','WS','TEAM_CONF_RANK']]
    train_noise, Y_train_noise = add_noise_mvp(train_imp, Y_train)
    regr = RandomForestRegressor(n_estimators= 1300, min_samples_split=10, min_samples_leaf= 4, max_features = 'auto', max_depth = 4, n_jobs= -1)
    regr.fit(train_noise, Y_train_noise)
    #regr.fit(train_imp, Y_train)
    pred = regr.predict(test_imp)
    res = test_imp
    res ['score MVP'] = Y_test
    res ['pred']= pred
    return pd.DataFrame(res)
    
        
  
