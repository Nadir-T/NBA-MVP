import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from fonctions_utiles import assign_rank, score_rank


doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'
doss_res = '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Résultats/'



df = pd.read_csv(doss + 'df.csv')
df = df.dropna(subset=['PER'])
players = df[['Player']]
#df = df.set_index(['Player'])
players = players.reset_index(drop=True)

years = df[['Year']]
scores = df[['score MVP']]
classe = df[['classé MVP']]

df = df[['PTS','BPM','VORP','PER','OWS','WS','TEAM_CONF_RANK']]   

df = df.reset_index(drop= True)

poly = PolynomialFeatures(2)
df_poly = pd.DataFrame(poly.fit_transform(df))      

df_poly = df_poly.reset_index(drop= True)

years = years.reset_index(drop=True)
scores = scores.reset_index(drop=True)
classe = classe.reset_index(drop=True)

#df_poly = df_poly.reset_index(drop=True)
df_poly['Player'] = players

df_poly['Year'] = years
df_poly['classé MVP'] = classe
df_poly['score MVP'] = scores
df_poly = df_poly.set_index(['Player'])
df_poly_scaled = df_scaled = fonctions_utiles.normalize_by_year(df_poly)
df_poly_scaled[0]=1





def hypothesis(X, theta): 
    """
        Calcul les prédictions en fonction de theta et de X.
    """
    return np.dot(X, theta) 
  
    
def gradient(X, y, theta): 
    """
        Calcule le gradient.
    """
    h = hypothesis(X, theta) 
    grad = np.dot(X.transpose(), (h - y)) 
    return grad 
  
def cost(X, y, theta): 
    """
        Calcul le résultat de la fonction de coût.
    """
    h = hypothesis(X, theta) 
    J = np.dot((h - y).transpose(), (h - y)) 
    J /= 2
    return J[0] 
  

def create_mini_batches(X, y, batch_size): 
    """
        Crée les mini-bacth utiles pour la descente de gradient.
    """
    mini_batches = [] 
    data = np.hstack((X, y)) 
    np.random.shuffle(data) 
    n_minibatches = data.shape[0] // batch_size 
    i = 0
    for i in range(n_minibatches + 1): 
        mini_batch = data[i * batch_size:(i + 1)*batch_size, :] 
        X_mini = mini_batch[:, :-1] 
        Y_mini = mini_batch[:, -1].reshape((-1, 1)) 
        mini_batches.append((X_mini, Y_mini)) 
    if data.shape[0] % batch_size != 0: 
        mini_batch = data[i * batch_size:data.shape[0]] 
        X_mini = mini_batch[:, :-1] 
        Y_mini = mini_batch[:, -1].reshape((-1, 1)) 
        mini_batches.append((X_mini, Y_mini)) 
    return mini_batches 
  

def MBGD(X, y, num_iters, learning_rate = 0.03, batch_size = 30): 
    """
        Descente de gradient à l'aide de mini-bacth.
    """
    theta = 0.001 * np.random.rand(X.shape[1], 1)
    error_list = [] 
    for itr in range(num_iters): 
        mini_batches = create_mini_batches(X, y, batch_size) 
        for mini_batch in mini_batches: 
            X_mini, y_mini = mini_batch 
            theta = theta - learning_rate * gradient(X_mini, y_mini, theta) 
            error_list.append(cost(X_mini, y_mini, theta)) 
    return theta, error_list 



def polynomial_regression(X, y, alpha, num_iters):
    """
        Entraine un modèle de régression linéaire sur (X,y) avec un learning rate alpha, 
        en faisant num_iters itérations de descente de gradient.
        alpha le learning rate pour la régression.
        num_iters le nombre d'itérations de descente de gradient.
    """
    theta, cost = MBGD(X, y, num_iters, alpha )
    return theta, cost



def reg_poly_year(df_scaled, alpha, num_iters, year):
    """
        Prédit le score avec une régression polynomiale pour les joueurs de l'année year.
        Entrainé sur toutes les autres années.
        alpha le learning rate pour la régression.
        num_iters le nombre d'itérations de descente de gradient.
    """
    test = df_scaled[df_scaled['Year'] == year]
    train = df_scaled[df_scaled['Year'] != year]
    Y_train = train[['score MVP']]
    Y_test = test[['score MVP']]
    train_imp = train[[i for i in range(0, 36)]]
    test_imp = test[[i for i in range(0, 36)]]
    train_noise, Y_train_noise = fonctions_utiles.add_noise_mvp(train_imp, Y_train)
    Y_train_noise = pd.DataFrame(Y_train_noise)
    theta, cost = polynomial_regression(train_noise, Y_train_noise, alpha, num_iters)
    y_pred = np.dot(test_imp,theta) 
    res = test_imp
    res ['score MVP'] = Y_test
    res ['pred']= y_pred
    #print(theta)
    return pd.DataFrame(res)




def evalue(df_scaled, alpha, num_iters):
    """
        Evalue le modèle de régression polynomiale.
    """
    score_array = np.zeros((36,4))
    for i in range(1982, 2018):
        print(i)
        full_res = reg_poly_year(df_scaled, alpha, num_iters, i)
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
    #df_score.to_csv(doss_res + 'score_' + 'Regression polynomiale' + '.csv', index =False)
    return df_score
    
    
    
    
    
    
    
    
    