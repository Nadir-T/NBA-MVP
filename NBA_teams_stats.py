import pandas as pd

from nba_api.stats.endpoints import teamyearbyyearstats    # API permettant d'obtenir diverses statistiques sur la NBA
from nba_api.stats.static import teams

pd.set_option('mode.chained_assignment', None)


def f_totale_team(seasons_stats, teams_stats):
    """
        Ajoute les statistiques de l'équipe à chacun des joueurs 
    """
    seasons_stats['Year'] = seasons_stats['Year'].apply(change_type)
    l = liste_teams()
    seasons_stats['TEAM_WINS'] = 0.
    seasons_stats['TEAM_LOSSES'] = 0.
    seasons_stats['TEAM_WIN_PCT'] = 0.
    seasons_stats['TEAM_CONF_RANK'] = 0.
    df = seasons_stats[seasons_stats['Year']>1981]   # On ne garde que les statistiques à partir de 1981
    df = merge(df, teams_stats)
    df = gere_tot(df)
    df = delete_tot(df)
    df['TEAM_WIN_PCT'] = df['TEAM_WINS'] / (df['TEAM_LOSSES'] + df['TEAM_WINS'])
    return df
    

def change_type(year):   
    """
        Change le type de l'année qui était un string en un int
    """
    return int(year)


def liste_teams():
    """
        Fonction de travail qui nous donne les id de toutes les équipes
    """
    liste_id = []
    liste_dic=[]
    for i in range(1940,2019):
        liste_dic += teams.find_teams_by_year_founded(i)
    for i in liste_dic:
        liste_id.append(i["id"])
    return liste_id




def fusion(l):
    """
        Crée une base comprenant toutes les statistiques pour chaque saisons pour toutes les équipes
    """
    buf = teamyearbyyearstats.TeamYearByYearStats(team_id=l[0])
    teams_stats = buf.get_data_frames()[0]
    for i in l[1::]:
        buf = teamyearbyyearstats.TeamYearByYearStats(team_id=i)
        df2 = buf.get_data_frames()[0]
        teams_stats = pd.concat([teams_stats, df2],ignore_index = True)
    return teams_stats



 
def change_year(year):
    """
        Change le format de l'année 
        Ex : 1987-88 devient 1988
    """
    new_year = year[0:2] + year[5:7]
    if new_year == "1900":
        new_year = "2000"
    return new_year
        


def correspondance(ind_team):
    """
        Dans la base des statistiques de joueurs, le nom de l'équipe est donné sous la forme d'un identifiant.
        Nous voulons donc faire correspondre cela avec le nom des équipes se trouvant dans la base de statistiques des équipes.
        Le problème est que les franchises peuvent se changer de ville ou être renommées et donc un identifiant dans la base des joueurs peut correspondre à différentes équipes dans la base des équipes.
        Heureusement cela n'est pas possible lors de la même année, donc on va toujours pouvoir identifier l'équipe d'un joueur grâce à l'identifiant de son équipe et de l'année.
        Alors on ajoute toutes les correspondances valables et on choisira la bonne par la suite.
        On rajoute aussi 'Tot' qui correspond aux joueurs ayant joué dans plusieurs équipes lors de la même année.
    """
    equipes = [['HOU', 'Rockets'],['MIL', 'Bucks'],['DET', 'Pistons'],['CHI', 'Bulls'],['KCO', 'Kings'],['PHO', 'Suns'],['NYK', 'Knicks'],['GSW', 'Warriors'],['ATL', 'Hawks'],['PHI', '76ers'],['CLE', 'Cavaliers'],['LAL', 'Lakers'],['SEA', 'SuperSonics'],['BOS', 'Celtics'],['BUF', 'Braves'],['CAP', 'Bullets'],['POR', 'Trail Blazers'],['TOT', 'Tot'],['NOJ', 'Jazz'],['WSB', 'Bullets'],['KCK', 'Kings'],['IND', 'Pacers'],['NYN', 'Nets'],['DEN', 'Nuggets'],['SAS', 'Spurs'],['NJN', 'Nets'],['SDC', 'Clippers'],['UTA', 'Jazz'],['DAL', 'Mavericks'],['LAC', 'Clippers'],['SAC', 'Kings'],['CHH', 'Hornets'],['MIA', 'Heat'],['ORL', 'Magic'],['MIN', 'Timberwolves'],['VAN', 'Grizzlies'],['TOR', 'Raptors'],['WAS', 'Wizards'],['WAS', 'Bullets'],['MEM', 'Grizzlies'],['NOH', 'Hornets'],['NOH', 'Pelicans'],['CHA', 'Hornets'],['CHA', 'Bobcats'],['NOK', 'Hornets'],['OKC', 'Thunder'],['BRK', 'Nets'],['NOP', 'Pelicans'],['CHO', 'Hornets']]
    corres = []
    for i in equipes:
        if i[0] == ind_team:
            corres.append(i[1])
    return corres

def merge(df, teams_stats):
    """
        Rajoute les statistiques de l'équipe à la plupart des joueurs
    """
    for i, row in df.iterrows():
        year = int(row['Year'])
        ind_team = row['Tm']
        corres = correspondance(ind_team)
        team = corres[0]    # On regarde la première correspondance d'équipe
        if team != 'Tot':                     # Quand c'est Tot on laisse les statistiques inchangées
            x = teams_stats[(teams_stats['YEAR'] == year) & (teams_stats['TEAM_NAME'] == team)]
            if len(x)==0:       # Dans ce cas cela signifie qu'on ne regarde pas la bonne équipe (comme expliqué plus haut)
                team = corres[1]   # Alors on regarde la deuxième équipe de la liste 
                x = teams_stats[(teams_stats['YEAR'] == year) & (teams_stats['TEAM_NAME'] == team)]
            if len(x)==0:
                team = correspondance(ind_team)[2]    # Si ce n'est toujours pas la bonne, on regarde la troisième (on sait qu'il n'y en a pas plus de trois au vu de la construction de correspondance)
                x = teams_stats[(teams_stats['YEAR'] == year) & (teams_stats['TEAM_NAME'] == team)]
            df.at[i, 'TEAM_WINS'] = x.iloc[0]['WINS']
            df.at[i, 'TEAM_LOSSES'] = x.iloc[0]['LOSSES']
            df.at[i, 'TEAM_WIN_PCT'] = x.iloc[0]['WIN_PCT']
            df.at[i, 'TEAM_CONF_RANK'] = x.iloc[0]['CONF_RANK']
    return df


def moy_pond(l_coef,l):
    """
        Calcule la moyenne pondérée.
        Les coefficients de pondérations se trouvent dans la première liste en paramètre.
    """
    res=0
    for i in range(len(l_coef)):
        res += l_coef[i] * l[i]
    return res/sum(l_coef)
        
       
def gere_tot(df):
    """
        Permet de gérer les statistiques des joueurs ayant joué dans plusieurs équipes lors d'une saisons.
        On va calculer les statistiques pour la ligne où l'équipe est 'Tot' avec une moyenne pondérée des 
        statistiques des équipes dans lequel le joueur a joué avec comme coefficient de pondération, le 
        nombre de matchs joués dans chaque équipe. Ceci est un choix de notre part.
    """
    for i, row in df.iterrows():
        if row['Tm']=='TOT':
            buf = df[(df['Player']==row['Player']) & (df['Year']==row['Year']) & (df['Tm'] != 'TOT')]  # On crée une base avec toutes les équipes dans lequel ils a joué durant la saison si il en a joué dans plusieurs
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

 

def delete_tot(df):
    """
        On supprime les lignes des joueurs (qui ont joué dans plusieurs équipes) autres que la 'Tot' 
        qui regroupe désormais les statistiques pondérées.
        Cette fonction n'est pas optimisée et il aurait sûrement mieux valu d'inclure ce travail dans
        la fonction précédente.
    """
    buf = df[df['Tm']=='TOT']
    for i, row in buf.iterrows():
        year = int(row['Year'])
        player = row['Player']
        df = df[(df['Year']!=year) | (df['Player']!=player) | (df['Tm']=='TOT')]
    return df

