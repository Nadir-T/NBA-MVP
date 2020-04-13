import pandas as pd
import numpy as np
import fonctions_utiles
import matplotlib.pyplot as plt

from lin_reg import reg_lin_year
from lin_reg_noise import reg_lin_year_noise
from class_reg import class_reg_year


doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'

df = pd.read_csv(doss + 'df.csv')
df = df.set_index(['Player'])

df_scaled = fonctions_utiles.normalize_by_year(df)
df_scaled = df_scaled.dropna(subset=['PER'])

#names = ['Linear regression', 'Linear regression with noise', 'Classification and linear regression']

#models = [reg_lin_year, reg_lin_noise_year, class_reg_year]

names = ['Linear regression with noise']

models = [reg_lin_year_noise]


def compare_models(alpha, num_iters):
    l_score = []
    for name, model in zip(names, models):
        score_array = np.zeros((36,4))
        for i in range(2010, 2018):
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
        df_score.to_csv(doss + 'score_' + name + '.csv', index =False)
        l_score.append(df_score)
    return l_score


