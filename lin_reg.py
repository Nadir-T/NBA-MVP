import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt
from fonctions_utiles import assign_rank, score_rank

doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'

df = pd.read_csv(doss + 'df.csv')
df = df.set_index(['Player'])

df_scaled = fonctions_utiles.normalize_by_year(df)
df_scaled = df_scaled.dropna(subset=['PER'])



def reg_lin_year(df_scaled, alpha, num_iters, year):
    test = df_scaled[df_scaled['Year'] == year]
    train = df_scaled[df_scaled['Year'] != year]
    Y_train = train['score MVP']
    Y_test = test['score MVP']
    train_imp = train[['PTS','TOV','FTA','VORP','PER','BPM','OWS','BLK','WS','TEAM_CONF_RANK']]   
    test_imp = test[['PTS','TOV','FTA','VORP','PER','BPM','BLK','OWS','WS','TEAM_CONF_RANK']]
    theta, cost = linear_regression(train_imp, Y_train, alpha, num_iters)
    one_column = np.ones((test_imp.shape[0],1))
    test_bis = np.concatenate((one_column, test_imp), axis = 1)
    y_pred = np.dot(test_bis,np.transpose(theta)) 
    res = test_imp
    res ['score MVP'] = Y_test
    res ['pred']= y_pred
    return pd.DataFrame(res)

def hypo(theta, X, n):
    h = np.ones((X.shape[0],1))
    theta = theta.reshape(1,n+1)
    for i in range(0,X.shape[0]):
        h[i] = float(np.matmul(theta, X[i]))
    h = h.reshape(X.shape[0])
    return h

def BGD(theta, alpha, num_iters, h, X, y, n):
    cost = np.ones(num_iters)
    for i in range(0,num_iters):
        theta[0] -= (alpha/X.shape[0]) * sum(h - y)
        for j in range(1,n+1):
            theta[j] = theta[j] - (alpha/X.shape[0]) * sum((h-y) * X.transpose()[j])
        h = hypo(theta, X, n)
        cost[i] = (1/X.shape[0]) * 0.5 * sum(np.square(h - y))
    theta = theta.reshape(1,n+1)
    return theta, cost

def linear_regression(X, y, alpha, num_iters):
    n = X.shape[1]
    one_column = np.ones((X.shape[0],1))
    X = np.concatenate((one_column, X), axis = 1)
    theta = 0.1 + 0.1*np.random.randn(n+1)  
    h = hypo(theta, X, n)
    theta, cost = BGD(theta,alpha,num_iters,h,X,y,n)
    return theta, cost



