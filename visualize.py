import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
fig = plt.figure()
ax = plt.axes(projection='3d')

doss =  '/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/'



df = pd.read_csv(doss + 'df.csv')
stats_clean = pd.read_csv(doss + 'stats_clean.csv')

players = stats_clean[(stats_clean['Year']>2007) & (stats_clean['Year']<=2017)]

players['PTS/G'] = players['PTS']/ players['G']

mvp =  players[players['classé MVP']==1]
non_mvp =  players[players['classé MVP']==0]



l01 = non_mvp['PTS'].tolist()
l02 = non_mvp['WS'].tolist()
l11 = mvp['PTS'].tolist()
l12 = mvp['WS'].tolist()

plt.plot(l11,l12,'ro')
plt.plot(l01,l02,'bo')
plt.show()


players = stats_clean[(stats_clean['Year']>2007) & (stats_clean['Year']<=2017)]

players['PTS/G'] = players['PTS']/ players['G']

mvp =  players[players['classé MVP']==1]
non_mvp =  players[players['classé MVP']==0]



l01 = non_mvp['PTS'].to_numpy()
l02 = non_mvp['WS'].to_numpy()
l03 = non_mvp['TEAM_WIN_PCT'].to_numpy()
l11 = mvp['PTS'].to_numpy()
l12 = mvp['WS'].to_numpy()
l13 = mvp['TEAM_WIN_PCT'].to_numpy()

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(l01, l02, l03, 'bo')
ax.scatter3D(l11, l12, l13, 'ro')


corr_matrix = stats_clean.corr()
corr_matrix['score MVP'].sort_values()

corr_matrix = stats_clean.corr(method = 'kendall')
corr_matrix['score MVP'].sort_values()

corr_matrix = stats_clean.corr(method = 'spearman')   # Le mieux dans notre cas
corr_matrix['score MVP'].sort_values()


