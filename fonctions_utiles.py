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

#Normalisation par année

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler() 

def normalize_by_year(df):
    df_scaled = pd.DataFrame(columns = df.columns)
    A = df.drop(['classé MVP','score MVP', 'Year'], axis = 1) #on enlève les colonnes qu'on ne normalise pas
    for k in range(1982, 2018):
        B = pd.DataFrame(scaler.fit_transform(A[df['Year']==k]), index = A[df['Year']==k].index, columns = A.columns)
        B['Year'] = k   #On rajoute les colonnes enlevés
        C = df[df['Year'] == k]
        B['classé MVP'] = C['classé MVP']
        B['score MVP'] = C['score MVP']
        B = B[df.columns]   #On remet les colonnes dans l'ordre
        df_scaled = B.append(df_scaled)
    return df_scaled
