import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt
from statistics import mean
from sklearn.svm import SVC
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


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


def SVC_linear(X_train, Y_train, X_test, Y_test, score_mvp, c=1):
    svclassifier = SVC(kernel='linear', C=c)
    svclassifier.fit(X_train, Y_train)
    y_pred = svclassifier.predict(X_test)
    res = X_test
    res['score'] = score_mvp
    res ['classé'] = Y_test
    res ['pred']= y_pred
    return res

def SVC_poly(X_train, Y_train, X_test, Y_test, score_mvp, c=1):
    svclassifier = SVC(kernel='poly', degree = 2, C=c)
    svclassifier.fit(X_train, Y_train)
    y_pred = svclassifier.predict(X_test)
    res = X_test
    res['score'] = score_mvp
    res ['classé'] = Y_test
    res ['pred']= y_pred
    return res

def SVC_sigmoid(X_train, Y_train, X_test, Y_test, score_mvp, c=1):
    svclassifier = SVC(kernel='sigmoid', C=c)
    svclassifier.fit(X_train, Y_train)
    y_pred = svclassifier.predict(X_test)
    res = X_test
    res['score'] = score_mvp
    res ['classé'] = Y_test
    res ['pred']= y_pred
    return res

def SVC_RBF(X_train, Y_train, X_test, Y_test, score_mvp, c=1):
    svclassifier = SVC(kernel='rbf', C=c)
    svclassifier.fit(X_train, Y_train)
    y_pred = svclassifier.predict(X_test)
    res = X_test
    res['score'] = score_mvp
    res ['classé'] = Y_test
    res ['pred']= y_pred
    return res

def QDA(X_train, Y_train, X_test, Y_test, score_mvp, c=1):
    clf = QuadraticDiscriminantAnalysis()
    clf.fit(X_train, Y_train)
    y_pred = clf.predict(X_test)
    res = X_test
    res['score'] = score_mvp
    res ['classé'] = Y_test
    res ['pred']= y_pred
    return res



def confusion_matrix(y,y_pred):
    """
        Renvoie la matrice de confusion.
    """
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
    
            
def predict_score(X_train, Y_train, X_test, Y_test, score_mvp, classifier, c=1):   
    res = classifier(X_train, Y_train, X_test, Y_test, score_mvp, c)
    y = res['classé']
    y_pred = res['pred']
    mat = confusion_matrix(y,y_pred)
    recall = mat[0,0]/(mat[0,0]+mat[0,1])
    precision = mat[0,0]/(mat[0,0]+mat[1,0])
    return mat, recall, precision, 2*precision*recall/(precision+recall)
    
    
def test_aleatoire(df_scaled, nb, c=1):
    """
        Test nb fois aléatoirement la performance du classificateur entrainé sur 31 saisons 
        et testés sur 5 saisons.
    """
    sum_recall = 0
    sum_precision = 0
    sum_f1 = 0
    l_res = []
    for i in range(nb):
        test, train = fonctions_utiles.coupe_by_year(df_scaled, 5)
        Y_train = train['classé MVP']
        Y_test = test['classé MVP']
        score_mvp = test['score MVP']
        train_imp = train[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]   
        test_imp = test[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]
        train_noise, Y_train_noise = fonctions_utiles.add_noise_mvp(train_imp, Y_train)
        Y_train_noise = pd.DataFrame(Y_train_noise)
        Y_train_noise['classé MVP'] = Y_train_noise['classé MVP'].astype(int)
        mat, recall, precision, f1 = predict_score(train_noise, Y_train_noise, test_imp, Y_test, score_mvp, SVC_poly, c)
        sum_recall += recall
        sum_precision += precision
        sum_f1 += f1
        l_res.append([mat, recall, precision, f1])
    return l_res, sum_recall/nb, sum_precision/nb, sum_f1/nb

num = [0,1,2,3,4]  
name = ['SVC_linear', 'SVC_poly', 'SVC_sigmoid', 'SVC_RBF', 'QDA']
classifiers = [SVC_linear, SVC_poly, SVC_sigmoid, SVC_RBF, QDA]

def compare_classifiers(df_scaled, nb):
    """
        Compare les 5 classificateurs en testant aléatoirement nb fois.
    """
    res = np.zeros((5,4))
    for i in range(nb):
        test, train = fonctions_utiles.coupe_by_year(df_scaled, 5)     # Le test se compose de 5 années.
        for j, nom, classifier in zip(num, name, classifiers):
            Y_train = train['classé MVP']
            Y_test = test['classé MVP']
            score_mvp = test['score MVP']
            train_imp = train[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]   
            test_imp = test[['PTS','PER','BPM','VORP','OWS','WS','TEAM_CONF_RANK']]
            train_noise, Y_train_noise = fonctions_utiles.add_noise_mvp(train_imp, Y_train)
            Y_train_noise = pd.DataFrame(Y_train_noise)
            Y_train_noise['classé MVP'] = Y_train_noise['classé MVP'].astype(int)
            print(i, nom)
            mat, recall, precision, f1 = predict_score(train_noise, Y_train_noise, test_imp, Y_test, score_mvp, classifier, c=1)
            res[j, 1:4] += np.array([recall, precision, f1])
    res = res / nb
    res = pd.DataFrame(res, columns =['Classifier', 'Recall', 'Precision', 'F1'])
    res['Classifier'] = name
    return res    
            
            
### On se rend compte que le meilleur classifier est le SVC poly, on va essayer de l'améliorer encore 
    
def choose_regu(df_scaled, nb): 
    """
        Essaye différent paramètre de régularisation.
    """
    l = [0.1, 0.2, 0.5, 1, 2, 5, 10]      
    l_recall = []
    l_precision = []
    l_f1 = []
    for c in l:
        print(c)
        l_res, recall, precision, f1 = test_aleatoire(df_scaled, nb, c)
        l_recall.append(recall)
        l_precision.append(precision)
        l_f1.append(f1)
    plt.plot(l, l_recall, 'r-')
    plt.plot(l, l_precision, 'b-')
    plt.plot(l, l_f1, 'g-')
    plt.show()
    
    
    
    
    
    
