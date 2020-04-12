import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt
from statistics import mean
from sklearn.svm import SVC
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF


doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'

df = pd.read_csv(doss + 'df.csv')
df = df.set_index(['Player'])

df_scaled = fonctions_utiles.normalize_by_year(df)
df_scaled = df_scaled.dropna(subset=['PER'])
test, train = fonctions_utiles.coupe_by_year(df_scaled, 1)

Y_train = train['classé MVP']
Y_test = test['classé MVP']

score_mvp = test['score MVP']

train_imp = train[['PTS','PER','FTA','VORP','OWS','WS','TEAM_CONF_RANK']]   
test_imp = test[['PTS','PER','FTA','VORP','OWS','WS','TEAM_CONF_RANK']]

train_noise, Y_train_noise = fonctions_utiles.add_noise_mvp_2(train_imp, Y_train)
Y_train_noise = pd.DataFrame(Y_train_noise)
Y_train_noise['classé MVP'] = Y_train_noise['classé MVP'].astype(int)

def predict_SVC(X_train, Y_train, X_test, Y_test, score_mvp, c=1):
    svclassifier = SVC(kernel='rbf', degree = 3, C=c)
    svclassifier.fit(X_train, Y_train)
    y_pred = svclassifier.predict(X_test)
    res = X_test
    res['score'] = score_mvp
    res ['classé'] = Y_test
    res ['pred']= y_pred
    return res

def predict_QDA(X_train, Y_train, X_test, Y_test, score_mvp):
    clf = QuadraticDiscriminantAnalysis()
    clf.fit(X_train, Y_train)
    y_pred = clf.predict(X_test)
    res = X_test
    res['score'] = score_mvp
    res ['classé'] = Y_test
    res ['pred']= y_pred
    return res

def predict_GPC(X_train, Y_train, X_test, Y_test, score_mvp):
    clf = GaussianProcessClassifier(1.0 * RBF(1.0))
    clf.fit(X_train, Y_train)
    y_pred = clf.predict(X_test)
    res = X_test
    res['score'] = score_mvp
    res ['classé'] = Y_test
    res ['pred']= y_pred
    return res

def confusion_matrix(y,y_pred):
    mat = np.zeros((2,2), dtype=int)
    for i in range(len(y)):
        if y[i]==0:
            if y_pred[i]==0:
                mat[1,1]+=1
            else:
                mat[1,0]+=1
        else:
            if y_pred[i]==0:
                mat[0,1]+=1
            else:
                mat[0,0]+=1
    return mat
    
            
def predict_score(X_train, Y_train, X_test, Y_test, score_mvp, c=1):    # Nous on veut surtout un très haut recall, pour ne pas passer à côté de MVP
    res = predict_SVC(X_train, Y_train, X_test, Y_test, score_mvp, c)
    y = res['classé']
    y_pred = res['pred']
    mat = confusion_matrix(y,y_pred)
    recall = mat[0,0]/(mat[0,0]+mat[0,1])
    precision = mat[0,0]/(mat[0,0]+mat[1,0])
    return mat, recall, precision, 2*precision*recall/(precision+recall)
    
    
def test_aleatoire(df_scaled, nb, c=1):
    sum_recall = 0
    sum_precision = 0
    sum_f1 = 0
    l_res = []
    for i in range(nb):
        test, train = fonctions_utiles.coupe_by_year(df_scaled, 5)
        Y_train = train['classé MVP']
        Y_test = test['classé MVP']
        score_mvp = test['score MVP']
        train_imp = train[['PTS','PER','FTA','TOV','VORP','OWS','WS','TEAM_CONF_RANK']]   
        test_imp = test[['PTS','PER','FTA','TOV','VORP','OWS','WS','TEAM_CONF_RANK']]
        train_noise, Y_train_noise = fonctions_utiles.add_noise_mvp_2(train_imp, Y_train)
        Y_train_noise = pd.DataFrame(Y_train_noise)
        Y_train_noise['classé MVP'] = Y_train_noise['classé MVP'].astype(int)
        mat, recall, precision, f1 = predict_score(train_noise, Y_train_noise, test_imp, Y_test, score_mvp, c)
        sum_recall += recall
        sum_precision += precision
        sum_f1 += f1
        l_res.append([mat, recall, precision, f1])
    return l_res, sum_recall/nb, sum_precision/nb, sum_f1/nb
    
### On se rend compte que le meilleur classifier est le SVC RBF, on va essayer de l'améliorer encore 
    
def choose_regu(df_scaled, nb):
    l=[0.005,0.01,0.02,0.03,0.05]      # Finalement 0.05 est le meilleur C
    l_recall = []
    l_precision = []
    l_f1 = []
    for c in l:
        l_res, recall, precision, f1 = test_aleatoire(df_scaled, nb, c)
        l_recall.append(recall)
        l_precision.append(precision)
        l_f1.append(f1)
    plt.plot(l, l_recall, 'r-')
    plt.plot(l, l_precision, 'b-')
    plt.plot(l, l_f1, 'g-')
    plt.show()
    
    
    
    
    
    
    
    