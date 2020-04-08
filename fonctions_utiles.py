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

def coupe_by_year(df):
    l = 1982 + np.random.choice(36, 1, replace=False)
    test = df[df['Year'].isin(l)]
    train = df[~df['Year'].isin(l)]
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






def assign_rank(l):
    l_rank = []
    for i in l:
        buf = 1
        for j in l:
            if j>i:
                buf+=1
        l_rank.append([i,buf])
    return l_rank

def score_rank(y,y_p):
    y_rank = assign_rank(y)
    y_p_rank = assign_rank(y_p)
    score = 0
    for i in range(len(y_rank)):
        if y_rank[i][0] != 0:
            score += (y_rank[i][1]-y_p_rank[i][1])**2
    return score
 
    
### BATCH GRADIENT DESCENT ###

def h(theta, X, n):
    h = np.ones((X.shape[0],1))
    theta = theta.reshape(1,n+1)
    for i in range(0,X.shape[0]):
        h[i] = float(np.matmul(theta, X[i]))
    h = h.reshape(X.shape[0])
    return h

def BGD(theta, alpha, num_iters, h, X, y, n):
    cost = np.ones(num_iters)
    for i in range(0,num_iters):
        theta[0] = theta[0] - (alpha/X.shape[0]) * sum(h - y)
        for j in range(1,n+1):
            theta[j] = theta[j] - (alpha/X.shape[0]) * sum((h-y) * X.transpose()[j])
        h = hypothesis(theta, X, n)
        cost[i] = (1/X.shape[0]) * 0.5 * sum(np.square(h - y))
    theta = theta.reshape(1,n+1)
    return theta, cost

    #fonction à appeler en pratique : 
def linear_regression(X, y, alpha, num_iters):
    n = X.shape[1]
    one_column = np.ones((X.shape[0],1))
    X = np.concatenate((one_column, X), axis = 1)
    theta = 0.1*np.random.randn(n+1)  #j'ai fait ce choix arbitraire peut-être à modifier
    h = hypothesis(theta, X, n)
    theta, cost = BGD(theta,alpha,num_iters,h,X,y,n)
    return theta, cost




def add_noise_mvp(train, Y_train):    # Y_train doit être une series si c'est déjà un DataFrame, enlever la première ligne
    Y_train = pd.DataFrame(Y_train)
    train['score MVP']=Y_train
    train_mvp = train[train['score MVP']>0]
    Y_train_mvp = Y_train[Y_train['score MVP']>0]
    train_mvp = train_mvp.drop(['score MVP'], axis = 1)
    mu, sigma = 0, 0.01 
    train = train.drop(['score MVP'], axis = 1)
    res_noise = train
    res_Y = Y_train
    for i in range(9):
        noise = np.random.normal(mu, sigma, train_mvp.shape)
        train_mvp_noise = train_mvp + noise
        res_noise = pd.concat([res_noise, train_mvp_noise])
        res_Y = pd.concat([res_Y, Y_train_mvp])    
    res_Y = res_Y['score MVP']
    return res_noise, res_Y


