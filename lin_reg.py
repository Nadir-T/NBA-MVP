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
    """
        Prédit le score avec une régression linéaire pour les joueurs de l'année year.
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
    theta, cost = linear_regression(train_imp, Y_train, alpha, num_iters)
    one_column = np.ones((test_imp.shape[0],1))
    test_bis = np.concatenate((one_column, test_imp), axis = 1)
    y_pred = np.dot(test_bis,np.transpose(theta)) 
    res = test_imp
    res ['score MVP'] = Y_test
    res ['pred']= y_pred
    return pd.DataFrame(res)

def hypo(theta, X, n):
    """
        Calcul les prédictions en fonction de theta et de X.
    """
    h = np.ones((X.shape[0],1))
    theta = theta.reshape(1,n+1)
    for i in range(0,X.shape[0]):
        h[i] = float(np.matmul(theta, X[i]))
    h = h.reshape(X.shape[0])
    return h

def BGD(theta, alpha, num_iters, h, X, y, n):
    """
        Batch gradient descent
    """
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
        """
        Entraine un modèle de régression linéaire sur (X,y) avec un learning rate alpha, 
        en faisant num_iters itérations de descente de gradient.
        alpha le learning rate pour la régression.
        num_iters le nombre d'itérations de descente de gradient.
    """
    n = X.shape[1]
    one_column = np.ones((X.shape[0],1))
    X = np.concatenate((one_column, X), axis = 1)
    theta = np.array([ 0.0210334, 0.00483984, -0.03282339,  0.07415321, 0.02219311,  0.01558913, -0.01884284, -0.00744582])
    h = hypo(theta, X, n)
    theta, cost = BGD(theta,alpha,num_iters,h,X,y,n)
    return theta, cost



def plot_J(train, y, alpha, num_iters, test, y_test, iter_min):  # iter_min permet d'afficher la courbe uniquement à partir de iter_min
    """
        Fonction affichant le coût des prédictions sur le dataset de train et celui de test
        en fonction du nombre d'itérations de la descente de gradient.
        Nous permet de savoir si notre nombre d'itérations est suffisant.
        Mais aussi de savoir si on overfit ou pas en vérifiant la différence entre le coût 
        sur la base de test et celui sur la base de train.
    """
    n = train.shape[1]                                           
    one_column = np.ones((train.shape[0],1))
    train = np.concatenate((one_column, train), axis = 1)
    one_column = np.ones((test.shape[0],1))
    test = np.concatenate((one_column, test), axis = 1)
    theta = 0.1 + 0.1*np.random.randn(n+1)
    cost_train = np.ones(num_iters)
    cost_test = np.ones(num_iters)
    h = hypo(theta, train, n)
    for i in range(0,num_iters):
        theta[0] -= (alpha/train.shape[0]) * sum(h - y)
        for j in range(1,n+1):
            theta[j] = theta[j] - (alpha/train.shape[0]) * sum((h-y) * train.transpose()[j])
        h = hypo(theta, train, n)
        cost_train[i] = (1/train.shape[0]) * 0.5 * sum(np.square(h - y))
        h_test = hypo(theta, test, n)
        cost_test[i] = (1/test.shape[0]) * 0.5 * sum(np.square(h_test - y_test))
    l = [i for i in range(iter_min,num_iters)]
    plt.plot(l,cost_train[iter_min::], 'ro')
    plt.plot(l,cost_test[iter_min::], 'bo')
    plt.show()


