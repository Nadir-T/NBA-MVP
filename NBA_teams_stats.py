import pandas as pd

from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.static import teams

pd.set_option('mode.chained_assignment', None)


def f_totale_team(seasons_stats, teams_stats):
    seasons_stats['Year'] = seasons_stats['Year'].apply(change_type)
    l = liste_teams()
    seasons_stats['TEAM_WINS'] = 0.
    seasons_stats['TEAM_LOSSES'] = 0.
    seasons_stats['TEAM_WIN_PCT'] = 0.
    seasons_stats['TEAM_CONF_RANK'] = 0.
    df = seasons_stats[seasons_stats['Year']>1973]
    df = merge(df, teams_stats)
    df = gere_tot(df)
    df['TEAM_WIN_PCT'] = df['TEAM_WINS'] / (df['TEAM_LOSSES'] + df['TEAM_WINS'])
    return df
    

def change_type(year):   # Le type était merdique, maintenant c'est un entier
    return int(year)


def liste_teams():
    liste_id = []
    liste_dic=[]
    for i in range(1940,2019):
        liste_dic += teams.find_teams_by_year_founded(i)
    for i in liste_dic:
        liste_id.append(i["id"])
    return liste_id




def fusion(l):
    buf = teamyearbyyearstats.TeamYearByYearStats(team_id=l[0])
    teams_stats = buf.get_data_frames()[0]
    for i in l[1::]:
        buf = teamyearbyyearstats.TeamYearByYearStats(team_id=i)
        df2 = buf.get_data_frames()[0]
        teams_stats = pd.concat([teams_stats, df2],ignore_index = True)
    return teams_stats



 
def change_year(year):
    new_year = year[0:2] + year[5:7]
    if new_year == "1900":
        new_year = "2000"
    return new_year
        



def correspondance(ind_team):
    equipes = [['HOU', 'Rockets'],['MIL', 'Bucks'],['DET', 'Pistons'],['CHI', 'Bulls'],['KCO', 'Kings'],['PHO', 'Suns'],['NYK', 'Knicks'],['GSW', 'Warriors'],['ATL', 'Hawks'],['PHI', '76ers'],['CLE', 'Cavaliers'],['LAL', 'Lakers'],['SEA', 'SuperSonics'],['BOS', 'Celtics'],['BUF', 'Braves'],['CAP', 'Bullets'],['POR', 'Trail Blazers'],['TOT', 'Tot'],['NOJ', 'Jazz'],['WSB', 'Bullets'],['KCK', 'Kings'],['IND', 'Pacers'],['NYN', 'Nets'],['DEN', 'Nuggets'],['SAS', 'Spurs'],['NJN', 'Nets'],['SDC', 'Clippers'],['UTA', 'Jazz'],['DAL', 'Mavericks'],['LAC', 'Clippers'],['SAC', 'Kings'],['CHH', 'Hornets'],['MIA', 'Heat'],['ORL', 'Magic'],['MIN', 'Timberwolves'],['VAN', 'Grizzlies'],['TOR', 'Raptors'],['WAS', 'Wizards'],['WAS', 'Bullets'],['MEM', 'Grizzlies'],['NOH', 'Hornets'],['NOH', 'Pelicans'],['CHA', 'Hornets'],['CHA', 'Bobcats'],['NOK', 'Hornets'],['OKC', 'Thunder'],['BRK', 'Nets'],['NOP', 'Pelicans'],['CHO', 'Hornets']]
    corres = []
    for i in equipes:
        if i[0] == ind_team:
            corres.append(i[1])
    corres.append('Tot')
    return corres

def merge(df, teams_stats):
    for i, row in df.iterrows():
        year = int(row['Year'])
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
    return df


def moy_pond(l_coef,l):
    res=0
    for i in range(len(l_coef)):
        res += l_coef[i] * l[i]
    return res/sum(l_coef)
        
       
def gere_tot(df):
    for i, row in df.iterrows():
        if row['Tm']=='TOT':
            buf = df[(df['Player']==row['Player']) & (df['Year']==row['Year']) & (df['Tm'] != 'TOT')]
            l_g = []
            l_w = []
            l_l = []
            l_r = []
            for j, row2 in buf.iterrows():
                l_g.append(row2['G'])
                l_w.append(row2['TEAM_WINS'])
                l_l.append(row2['TEAM_LOSSES'])
                l_r.append(row2['TEAM_CONF_RANK'])
            df.at[i, 'TEAM_WINS'] = moy_pond(l_g,l_w)
            df.at[i, 'TEAM_LOSSES'] = moy_pond(l_g,l_l)
            df.at[i, 'TEAM_CONF_RANK'] = moy_pond(l_g,l_r)
    return df

 










