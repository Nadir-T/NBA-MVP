import pandas as pd
import numpy as np
from sklearn.utils import shuffle

doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'

df = pd.read_csv(doss + 'df.csv')
stats_clean = pd.read_csv(doss + 'stats_clean.csv')

### Fonctions à faire ###
# - normalise par années
# - descente de gradient
# - calcul du cout avec anomaly detection
# - séparation train validation test
# - il faut penser à supprimer ceux qui ont un tot

def coupe(df):
    prop = len(df[df['score MVP']>0])/len(df)
    mvp =  df[df['score MVP']>0]
    non_mvp =  df[df['score MVP']==0]
    mvp_shuffle = shuffle(mvp)
    non_mvp_shuffle = shuffle(non_mvp)
    mvp_train = mvp_shuffle.iloc[:int(0.8*len(mvp_shuffle)),:]
    mvp_test = mvp_shuffle.iloc[int(0.8*len(mvp_shuffle)):,:]
    non_mvp_train = non_mvp_shuffle.iloc[:int(0.8*len(non_mvp_shuffle)),:]
    non_mvp_test = non_mvp_shuffle.iloc[int(0.8*len(non_mvp_shuffle)):,:]
    test = pd.concat([mvp_test, non_mvp_test], ignore_index=True)
    train = pd.concat([mvp_train, non_mvp_train], ignore_index=True)
    return test, train
    