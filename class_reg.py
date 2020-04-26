import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from classification import SVC_poly
from reg_lin import predict, linear_regression
from fonctions_utiles import assign_rank, score_rank

doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'

df = pd.read_csv(doss + 'df.csv')
df = df.set_index(['Player'])

df_scaled = fonctions_utiles.normalize_by_year(df)
df_scaled = df_scaled.dropna(subset=['PER'])


def train_reg_mvp(train, alpha, num_iters):
    """
        Entraine un modèle de régression linéaire sur les classés MVP.
    """
    train_mvp = train[train['score MVP']>0]
    Y_train_mvp = train_mvp['score MVP']
    train_imp = train_mvp[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]  
    theta, cost = linear_regression(train_imp, Y_train_mvp, alpha, num_iters)
    return theta

def class_reg(df_scaled, alpha, num_iters):
    """
        Prédit le score avec la méthode classification-régression pour les joueurs d'une année au hasard.
        Entrainé sur toutes les autres années.
        alpha le learning rate pour la régression.
        num_iters le nombre d'itérations de descente de gradient.
    """
    test, train = fonctions_utiles.coupe_by_year(df_scaled, 1)
    theta = train_reg_mvp(train, alpha, num_iters)
    Y_train = train['classé MVP']
    Y_train = pd.DataFrame(Y_train)
    Y_train['classé MVP'] = Y_train['classé MVP'].astype(int)
    Y_test = test['classé MVP']
    score_mvp = test['score MVP']
    train_imp = train[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]   
    X_test = test[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]
    X_train_noise, Y_train_noise = fonctions_utiles.add_noise_mvp_2(train_imp, Y_train)
    res_tot = SVC_poly(X_train_noise, Y_train_noise, X_test, Y_test, score_mvp)
    res_class = res_tot[res_tot['pred']==1]
    class_pred = res_class['pred']
    class_score = res_class['score']
    res_class = res_class[['PTS','PER','FTA','VORP','OWS','WS','TEAM_CONF_RANK']]  
    one_column = np.ones((res_class.shape[0],1))
    res_bis = np.concatenate((one_column, res_class), axis = 1)
    y_pred = np.dot(res_bis,np.transpose(theta)) 
    res = res_class
    res['score'] = class_score
    res['score_pred']= y_pred
    return res

def class_reg_year(df_scaled, alpha, num_iters, year):
    """
        Prédit le score avec la méthode classification-régression pour les joueurs de l'année year.
        Entrainé sur toutes les autres années.
        alpha le learning rate pour la régression.
        num_iters le nombre d'itérations de descente de gradient.
    """
    test = df_scaled[df_scaled['Year'] == year]
    train = df_scaled[df_scaled['Year'] != year]
    theta = train_reg_mvp(train, alpha, num_iters)
    Y_train = train['classé MVP']
    Y_train = pd.DataFrame(Y_train)
    Y_train['classé MVP'] = Y_train['classé MVP'].astype(int)
    Y_test = test['classé MVP']
    score_mvp = test['score MVP']
    train_imp = train[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]   
    X_test = test[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]
    X_train_noise, Y_train_noise = fonctions_utiles.add_noise_mvp_2(train_imp, Y_train)
    res_tot = SVC_poly(X_train_noise, Y_train_noise, X_test, Y_test, score_mvp)
    res_class = res_tot[res_tot['pred']==1]
    class_pred = res_class['pred']
    class_score = res_class['score']
    res_class = res_class[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]  
    one_column = np.ones((res_class.shape[0],1))
    res_bis = np.concatenate((one_column, res_class), axis = 1)
    y_pred = np.dot(res_bis,np.transpose(theta)) 
    res = res_class
    res['score'] = class_score
    res['score_pred']= y_pred
    res = pd.DataFrame(res)
    full_res = test[['score MVP']]
    full_res['pred'] = 0
    for i, row in res.iterrows():
        full_res.loc[i, 'pred'] = row['score_pred']
    full_res = full_res[(full_res['pred'] != 0) | (full_res['score MVP'] != 0) ]
    return full_res


def score_class_reg(df_scaled, alpha, num_iters):
    """
        Teste la méthode sur chaque année entre 1982 et 2017.
        alpha le learning rate pour la régression.
        num_iters le nombre d'itérations de descente de gradient.
    """
    score_array = np.zeros((36,4))
    for i in range(1982, 2018):
        print(i)
        full_res = class_reg_year(df_scaled, alpha, num_iters, i)
        pred = full_res['pred'].tolist()
        score = full_res['score MVP'].tolist()
        rank_pred = assign_rank(pred)
        rank_score = assign_rank(score)
        buf_score, premier, podium = score_rank(rank_score, rank_pred)
        score_array[i-1982,0] = i
        score_array[i-1982,1] = buf_score
        score_array[i-1982,2] = premier
        score_array[i-1982,3] = podium
    df_score = pd.DataFrame(score_array, columns = ['Year', 'Score', 'Premier', 'Podium'])
    return df_score
    

def score_class_perf_reg(df_scaled, alpha, num_iters):
    """
        Teste la méthode si la classification était parfaite.
        alpha le learning rate pour la régression.
        num_iters le nombre d'itérations de descente de gradient.
    """
    score_array = np.zeros((36,4))
    for i in range(1982, 2018):
        print(i)
        df_scaled_mvp = df_scaled[df_scaled['score MVP']>0]
        test = df_scaled_mvp[df_scaled_mvp['Year'] == i]  
        score = test['score MVP']
        train = df_scaled_mvp[df_scaled_mvp['Year'] != i]
        theta = train_reg_mvp(train, alpha, num_iters)
        X_test = test[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]
        one_column = np.ones((X_test.shape[0],1))
        res_bis = np.concatenate((one_column, X_test), axis = 1)
        y_pred = np.dot(res_bis,np.transpose(theta)) 
        X_test['score'] = score
        X_test['score_pred']= y_pred
        X_test = pd.DataFrame(X_test)
        pred = X_test['score_pred'].tolist()
        score = X_test['score'].tolist()
        rank_pred = assign_rank(pred)
        rank_score = assign_rank(score)
        buf_score, premier, podium = score_rank(rank_score, rank_pred)
        score_array[i-1982,0] = i
        score_array[i-1982,1] = buf_score
        score_array[i-1982,2] = premier
        score_array[i-1982,3] = podium
    df_score = pd.DataFrame(score_array, columns = ['Year', 'Score', 'Premier', 'Podium'])
    return df_score
        
        
 
