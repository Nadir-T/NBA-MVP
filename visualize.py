import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'



df = pd.read_csv(doss + 'df.csv')
stats_clean = pd.read_csv(doss + 'stats_clean.csv')

players_2015 = stats_clean[stats_clean['Year']==2015]

players_2015['PTS/G'] = players_2015['PTS']/ players_2015['G']

mvp =  players_2015[players_2015['classé MVP']==1]
non_mvp =  players_2015[players_2015['classé MVP']==0]



l01 = non_mvp['PTS'].tolist()
l02 = non_mvp['WS'].tolist()
l11 = mvp['PTS'].tolist()
l12 = mvp['WS'].tolist()

plt.plot(l11,l12,'ro')
plt.plot(l01,l02,'bo')
plt.show()
