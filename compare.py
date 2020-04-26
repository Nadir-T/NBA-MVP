import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt

from lin_reg import reg_lin_year
from lin_reg_noise import reg_lin_year_noise
from class_reg import class_reg_year


doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'
doss_res = '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Résultats/'

df = pd.read_csv(doss + 'df.csv')
df = df.set_index(['Player'])

df_scaled = fonctions_utiles.normalize_by_year(df)
df_scaled = df_scaled.dropna(subset=['PER'])

names = ['Linear regression', 'Linear regression with noise', 'Classification and linear regression']

models = [reg_lin_year, reg_lin_noise_year, class_reg_year]


def compare_models(alpha, num_iters):
    """
        Compare les modèles sur le score, le premier et le podium pour chaque année
        entre 1982 et 2017.
    """
    l_score = []
    for name, model in zip(names, models):
        score_array = np.zeros((36,4))
        for i in range(1982, 2018):
            print(name, i)
            full_res = model(df_scaled, alpha, num_iters, i)
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
        df_score.to_csv(doss_res + 'score_' + name + '.csv', index =False)
        l_score.append(df_score)
    return l_score


res_lin_reg = pd.read_csv(doss_res + 'score_' + 'Linear regression' + '.csv')
res_lin_reg_noise = pd.read_csv(doss_res + 'score_' + 'Linear regression with noise' + '.csv')
res_class_reg_year = pd.read_csv(doss_res + 'score_' + 'Classification and linear regression' + '.csv') 
l_res = [res_lin_reg, res_lin_reg_noise, res_class_reg_year]


def flat(res):
    """
        Forme les coordonnées pour la fonction plot.
    """
    mat = res.as_matrix()
    l = []
    l_first = []
    l_podium = []
    for i in range(len(mat)):
        if mat[i,3] == 1:
            l_podium.append((mat[i,0], mat[i,1]))
        elif mat[i,2] == 1:
            l_first.append((mat[i,0], mat[i,1]))
        l.append(mat[i,1])
    return l, l_first, l_podium

    
def plot():
    """
        Affiche les résultats de chacune des méthodes.
        Les résultats se composent du score, des premiers bien prédits et des podium bien prédits.
    """
    colors = ['r-', 'b-', 'g-']
    years = [i for i in range(1982, 2018)]
    for color, res in zip(colors, l_res):
        l, l_first, l_podium = flat(res)
        x_first = [x[0] for x in l_first]
        y_first = [x[1] for x in l_first]
        x_podium = [x[0] for x in l_podium]
        y_podium = [x[1] for x in l_podium]
        plt.plot(years, l, color)
        plt.plot(x_first, y_first, 'm.')
        plt.plot(x_podium, y_podium, 'ko')
    plt.savefig(doss_res + 'img' + '.png', dpi = 400)
    plt.show()

