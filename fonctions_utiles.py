import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler

doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'

df = pd.read_csv(doss + 'df.csv')

def coupe(df):
    """
        Permet de diviser le dataset en deux datasets avec une proportion égale de MVP dans chaque dataset.
    """
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
    

def coupe_by_year(df, n_years=1):
    """
        Permet de couper le dataset en deux dataset en fonction des années.
        Le n_years permet de choisir de combien de saison on veut que notre dataset de test se compose.
    """
    l = 1982 + np.random.choice(36, n_years, replace=False)
    test = df[df['Year'].isin(l)]
    train = df[~df['Year'].isin(l)]
    return test, train


scaler = StandardScaler() 

def normalize_by_year(df):
    """
        Normalise les données année par année.
    """
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


def assign_rank(l):
    """
        Assigne un rang à chaque élément de la liste.
    """
    l_rank = []
    for i in l:
        buf = 1
        for j in l:
            if j>i:
                buf+=1
        l_rank.append([i,buf])
    return l_rank

def score_rank(y_rank,y_p_rank):
    """
        Renvoie le score (définit dans le rapport) entre deux listes, 1 si le premier est le bon, 
        1 si le podium est le bon.
    """
    score = 0
    pond = 0
    premier = 0
    podium = 0
    for i in range(len(y_rank)):
        if y_rank[i][0] != 0:
            score += (1/y_rank[i][1]) * abs(y_rank[i][1]-y_p_rank[i][1])
            pond += (1/y_rank[i][1])
            if y_rank[i][1] == 1:
                premier += (y_p_rank[i][1] == 1) * 1
                podium += (y_p_rank[i][1] == 1) * 1
            elif y_rank[i][1] == 2:
                podium += (y_p_rank[i][1] == 2) * 1
            elif y_rank[i][1] == 3:
                podium += (y_p_rank[i][1] == 3) * 1
    return score/pond, premier, (podium==3)*1
    
    
def add_noise_mvp(train, Y_train, k=19):
    """
        Permet d'ajouter des données bruitées au dataset de train et au Y.
        On rajoute le bruit uniquement sur les joueurs classés au MVP pour obtenir plus de MVP 
        et ainsi leur donner plus d'importance.  Le paramètre k=19 permet d'avoir environ le 
        même nombre de classés MVP que de non classés.
    """
    Y_train = pd.DataFrame(Y_train)
    train['score MVP']=Y_train
    train_mvp = train[train['score MVP']>0]
    Y_train_mvp = Y_train[Y_train['score MVP']>0]
    train_mvp = train_mvp.drop(['score MVP'], axis = 1)
    mu, sigma = 0, 0.01          # mu = 0 est assez logique, et on a choisi sigma en observant les données.
    train = train.drop(['score MVP'], axis = 1)
    res_noise = train
    res_Y = Y_train
    for i in range(k):
        noise = np.random.normal(mu, sigma, train_mvp.shape)
        train_mvp_noise = train_mvp + noise
        res_noise = pd.concat([res_noise, train_mvp_noise])
        res_Y = pd.concat([res_Y, Y_train_mvp])    
    res_Y = res_Y['score MVP']
    return res_noise, res_Y





