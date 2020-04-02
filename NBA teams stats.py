import pandas as pd
from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.static import teams

seasons_stats = pd.read_csv('/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/seasons_stats.csv')

def liste_teams():
    liste_id = []
    liste_dic=[]
    for i in range(1940,2019):
        liste_dic += teams.find_teams_by_year_founded(i)
    for i in liste_dic:
        liste_id.append(i["id"])
    return liste_id

l = liste_teams()



def fusion():
    buf =  teamyearbyyearstats.TeamYearByYearStats(team_id=l[0])
    teams_stats = buf.get_data_frames()[0]
    for i in l[1::]:
        buf =  teamyearbyyearstats.TeamYearByYearStats(team_id=i)
        df2 = buf.get_data_frames()[0]
        teams_stats = pd.concat([teams_stats, df2],ignore_index = True)
    return teams_stats

teams_stats = fusion()


 
def change_year(year):
    new_year = year[0:2] + year[5:7]
    if new_year == "1900":
        new_year = "2000"
    return new_year
        
teams_stats["YEAR"] =  teams_stats["YEAR"].apply(change_year)

seasons_stats['TEAM_WINS'] = 0
seasons_stats['TEAM_LOSSES'] = 0
seasons_stats['TEAM_WIN_PCT'] = 0
seasons_stats['TEAM_CONF_RANK'] = 0
seasons_stats['TEAM_PO_WINS'] = 0 
seasons_stats['TEAM_PO_LOSSES'] = 0 


liste = seasons_stats.Tm.unique()
df = seasons_stats[seasons_stats['Year']>1973]
liste = df.Tm.unique()
equipe=[]

for i in liste:
    equipe.append([i,''])
    
equipes = [['HOU', 'Rockets'],['MIL', 'Bucks'],['DET', 'Pistons'],['CHI', 'Bulls'],['KCO', 'Kings'],['PHO', 'Suns'],['NYK', 'Knicks'],['GSW', 'Warriors'],['ATL', 'Hawks'],['PHI', '76ers'],['CLE', 'Cavaliers'],['LAL', 'Lakers'],['SEA', 'SuperSonics'],['BOS', 'Celtics'],['BUF', 'Braves'],['CAP', 'Bullets'],['POR', 'Trail Blazers'],['TOT', 'Tot'],['NOJ', 'Jazz'],['WSB', 'Bullets'],['KCK', 'Kings'],['IND', 'Pacers'],['NYN', 'Nets'],['DEN', 'Nuggets'],['SAS', 'Spurs'],['NJN', 'Nets'],['SDC', 'Clippers'],['UTA', 'Jazz'],['DAL', 'Mavericks'],['LAC', 'Clippers'],['SAC', 'Kings'],['CHH', 'Hornets'],['MIA', 'Heat'],['ORL', 'Magic'],['MIN', 'Timberwolves'],['VAN', 'Grizzlies'],['TOR', 'Raptors'],['WAS', 'Wizards'],['WAS', 'Bullets'],['MEM', 'Grizzlies'],['NOH', 'Hornets'],['NOH', 'Pelicans'],['CHA', 'Hornets'],['CHA', 'Bobcats'],['NOK', 'Hornets'],['OKC', 'Thunder'],['BRK', 'Nets'],['NOP', 'Pelicans'],['CHO', 'Hornets']]

def correspondance(ind_team):
    corres = []
    for i in equipes:
        if i[0] == ind_team:
            corres.append(i[1])
    corres.append('Tot')
    return corres

def merge():
    for i, row in df.iterrows():
        year = str(int(row['Year']))
        ind_team = row['Tm']
        team = correspondance(ind_team)[0]
        if team != 'Tot':
            x = teams_stats[(teams_stats['YEAR'] == year) & (teams_stats['TEAM_NAME'] == team)]
            if len(x)==0:
                team = correspondance(ind_team)[1]
                x = teams_stats[(teams_stats['YEAR'] == year) & (teams_stats['TEAM_NAME'] == team)]
            if len(x)==0:
                team = correspondance(ind_team)[2]
                x = teams_stats[(teams_stats['YEAR'] == year) & (teams_stats['TEAM_NAME'] == team)]
            df.at[i, 'TEAM_WINS'] = x.iloc[0]['WINS']
            df.at[i, 'TEAM_LOSSES'] = x.iloc[0]['LOSSES']
            df.at[i, 'TEAM_WIN_PCT'] = x.iloc[0]['WIN_PCT']
            df.at[i, 'TEAM_CONF_RANK'] = x.iloc[0]['CONF_RANK']
            df.at[i, 'TEAM_PO_WINS'] = x.iloc[0]['PO_WINS']
            df.at[i, 'TEAM_PO_LOSSES'] = x.iloc[0]['PO_LOSSES']

merge()
df2 = df[(df['TEAM_WINS']==0) & (df['Tm'] != 'TOT')]

df['TEAM_WIN_PCT'] = df['TEAM_WINS'] / (df['TEAM_LOSSES'] + df['TEAM_WINS'])
    
        
df.to_csv('/Users/Coni/Desktop/ENSAE/1A/Projet informatique/Data/df.csv', index=False)










