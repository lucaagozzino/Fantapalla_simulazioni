#!/usr/bin/env python
# coding: utf-8

# In[367]:


import numpy as np
from sympy.utilities.iterables import multiset_permutations
import random
import copy
import glob
from IPython import display
import pandas as pd
quotazioni = pd.read_csv ('Quotazioni_Fantacalcio.csv')


import progressbar
#pbar = progressbar.progressbar()

# In[368]:

######################################################## START DEFAULT PARAMETERS
struttura_rosa = np.array([3, 8, 8, 6])
#this must contain all the allowed schemes

Formazioni = {
    '352': [1, 3, 5, 2],
    '343': [1, 3, 4, 3],
    '442': [1, 4, 4, 2],
    '541': [1, 5, 4, 1],
    '532': [1, 5, 3, 2],
    '433': [1, 4, 3, 3]
    #aggiungere tutte le altre formazioni
    }
Fasce_goal = np.array([66,  70,  84,  88,  92,  96, 100])
Fasce_modificatore = np.array([6. , 6.5, 7. , 7.5, 8. ])
Valori_modificatore = np.array([1, 3, 5, 6, 8])
rows_to_skip=[0,1,2,3,4]

N_squadre = 8

######################################################## END DEFAULT PARAMETERS
# In[369]:


def names(num_squadre):
    team_names = []
    teams = {}
    for i in range(1,num_squadre+1):
        team_names.append("Team " + str(i))
        teams[i] = "Team " + str(i)
    return [teams, team_names]


# In[370]:


#[teams, team_names] = names(N_squadre)


# In[371]:


def fixture_gen(teams):
    temp = copy.deepcopy(teams)
    var = []
    while len(temp)>1:
        idx = list(temp)
        j,k = random.sample(idx,2)
        var.append((temp.pop(j),temp.pop(k)))
    return var


# In[372]:


def genera_rose(struttura_rosa, num_squadre):
    
    giocatori = struttura_rosa*num_squadre
    tot_giocatori = sum(giocatori)
    
    [p,d,c,a] = giocatori
    por = np.array(range(1,p+1))
    dif = np.array(range(1,d+1))+p
    cen = np.array(range(1,c+1))+p+d
    att = np.array(range(1,a+1))+p+d+c
    
    rosa_por=np.random.choice(por,[struttura_rosa[0],num_squadre],replace=False)
    rosa_dif=np.random.choice(dif,[struttura_rosa[1],num_squadre],replace=False)
    rosa_cen=np.random.choice(cen,[struttura_rosa[2],num_squadre],replace=False)
    rosa_att=np.random.choice(att,[struttura_rosa[3],num_squadre],replace=False)
 
    rosa = np.append(rosa_por,rosa_dif,axis=0)
    rosa = np.append(rosa,rosa_cen,axis=0)
    rosa = np.append(rosa,rosa_att,axis=0)
    
    return rosa


# In[373]:


#gives back a dataframe with the top 200 players
def top_players(struttura_rosa, quotazioni, num_squadre):
    players = {}
    j = 1
    [p,c,d,a]=struttura_rosa*num_squadre
    for k, element in quotazioni.iterrows():    
        if element['R'] == 'P' and j<=p:
            players[j] = [j, element['Id'],element['Nome'],element['Qt. A']]
            j+=1          
        elif element['R'] == 'D' and j<=p+d:
            players[j] = [j, element['Id'],element['Nome'],element['Qt. A']]
            j+=1                      
        elif element['R'] == 'C' and j<=p+d+c:
            players[j] = [j, element['Id'],element['Nome'],element['Qt. A']]
            j+=1                      
        elif element['R'] == 'A' and j<=p+d+c+a:
            players[j] = [j, element['Id'],element['Nome'],element['Qt. A']]
            j+=1
    players=pd.DataFrame(players).T

    players = players.rename(columns = {0:'My Id',1:'FC Id', 2:'Nome', 3:'Quotazione'})
    return players


# In[374]:


#assigns the dictionary grade to the specific team players
def assign_grade(rose, grades_dict):
    n,m = np.shape(rose)
    grades = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            if rose[i,j] in grades_dict:
                grades[i,j] = grades_dict[rose[i,j]]
    return grades   


# In[375]:


def modificatore(voti_dif, valori, fasce):
    temp = 0
    media = np.average(voti_dif)
    for i in range(len(fasce)):
            if media >= fasce[i]:
                temp = valori[i]
    return temp


# In[376]:


#for the top 200 players, creates a dictionary mapping 'My Id' to 'voto'
def all_grades_dict(struttura_rosa, quotazioni, voti_giornata, num_squadre):
    players = top_players(struttura_rosa, quotazioni, num_squadre)
    temp_votes = {}
    for k in range(len(voti_giornata['Cod.'])):
        if voti_giornata['Cod.'][k] == 'Cod.' or voti_giornata['Cod.'][k] == 'GENOA' or voti_giornata['Cod.'][k] == 'INTER' or voti_giornata['Cod.'][k] =='JUVENTUS'or voti_giornata['Cod.'][k] =='LAZIO'or voti_giornata['Cod.'][k] =='LECCE'or voti_giornata['Cod.'][k] =='MILAN'or voti_giornata['Cod.'][k] =='NAPOLI'or voti_giornata['Cod.'][k] =='PARMA' or voti_giornata['Cod.'][k] =='ROMA' or voti_giornata['Cod.'][k] =='FIORENTINA'or voti_giornata['Cod.'][k] =='SAMPDORIA'or voti_giornata['Cod.'][k] =='SASSUOLO'or voti_giornata['Cod.'][k] =='SPAL' or voti_giornata['Cod.'][k] =='TORINO'or voti_giornata['Cod.'][k] =='GENOA'or voti_giornata['Cod.'][k] =='UDINESE'or voti_giornata['Cod.'][k] =='VERONA'or voti_giornata['Cod.'][k] =='BOLOGNA'or voti_giornata['Cod.'][k] =='BRESCIA'or voti_giornata['Cod.'][k] =='CAGLIARI'or voti_giornata['Cod.'][k] =='ATALANTA':
            continue
        for j in range(1,len(players['My Id'])+1):
            if players['FC Id'][j] == np.float(voti_giornata['Cod.'][k]):
                #print(voti_giornata['Cod.'][k])
                temp_votes[j]=voti_giornata['Voto'][k]
                if temp_votes[j] == '6*':
                    temp_votes[j]= '6'
    return temp_votes # struttura My Id: voto


# In[377]:


#formazioni and dict_voti_giornata (from all_grades_dict) must be dictionaries
def voti_max(rose, struttura_rosa, formazioni, dict_voti_giornata, teams,  num_squadre, valori, fasce):
    [P,D,C,A]=struttura_rosa
    
    voti_rosa = assign_grade(rose, dict_voti_giornata)
    
    voti ={}
    for k in range(num_squadre):
        voto = 0
        for f in formazioni.items():
            #da aggiungere: modificatore difesa
            [n_p,n_d,n_c,n_a] = f[1]
            
            idx_p = (-voti_rosa[0:P,k]).argsort()[:n_p]
            idx_d = (-voti_rosa[0+P:P+D,k]).argsort()[:n_d]+P
            idx_c = (-voti_rosa[0+P+D:C+P+D,k]).argsort()[:n_c]+P+D
            idx_a = (-voti_rosa[0+P+D+C:P+D+C+A,k]).argsort()[:n_a]+P+D+C

            idx_all = np.hstack((idx_p,idx_d,idx_c,idx_a))
            
            extra = 0
            l_temp = copy.deepcopy(voti_rosa[idx_d,k].tolist())
            l_temp = np.sort(l_temp)
            
            if n_d >=4 and (l_temp >= 6).sum()>=4:
                voti_mod = np.append(l_temp[-3:],voti_rosa[idx_p,k])
                extra = modificatore(voti_mod, valori, fasce)
               
            voto = max(voto,np.sum(voti_rosa[idx_all,k]) + extra)
            
        voti[teams[k+1]] = voto
    return voti #per ogni combinazione di rose trova il voto massimo di squadra per la giornata


# In[378]:


def goal_scored(voti_squadre, fasce_goal):
    team_goals={}
    for team, voto in voti_squadre.items():
        goals = 0
        for i in range(len(fasce_goal)):
            if voto >= fasce_goal[i]:
                goals = i+1
        team_goals[team] = goals
    return team_goals


# In[379]:


def points(fixtures, voti_squadre, fasce_goal):
    goals = goal_scored(voti_squadre, fasce_goal)
    points_temp = {}
    matches = len(fixtures)
    for m in range(matches):
        teams = fixtures[m]
        if goals[teams[0]] == goals[teams[1]]:
            points_temp[teams[0]]=1
            points_temp[teams[1]]=1
    
        elif goals[teams[0]] > goals[teams[1]]:
            points_temp[teams[0]]=3
            points_temp[teams[1]]=0
            
        elif goals[teams[0]] < goals[teams[1]]:
            points_temp[teams[0]]=0
            points_temp[teams[1]]=3
    return points_temp
        


# In[380]:


def id_toName(struttura_rosa, quotazioni, rose, num_squadre, team_names):
    topPlayers = top_players(struttura_rosa, quotazioni, num_squadre)
    rose_nomi=pd.DataFrame(columns=team_names, index=range(25))
    for team_name in team_names:
        temp_teams = []
        for Myid in rose[team_name]:
             temp_teams.append(topPlayers['Nome'][Myid])
        rose_nomi[team_name] = temp_teams
    return rose_nomi


# In[381]:


def all_quot_dict(struttura_rosa, quotazioni, num_squadre):
    players = top_players(struttura_rosa, quotazioni, num_squadre)
    temp_quot={}
    for idx in players['My Id']:
        temp_quot[idx] = players['Quotazione'][idx]
    return temp_quot # struttura My Id: voto


# In[382]:


def assign_quot(rose, quot_dict, team_names): 
    n,m = np.shape(rose)
    quot = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            if rose[i,j] in quot_dict:
                quot[i,j] =  quot_dict[rose[i,j]]
    quot_tot = pd.DataFrame(data=np.sum(quot,axis=0,keepdims=True),columns=team_names).T
    return quot_tot


# In[383]:


def simula_campionato(struttura_rosa, team_names, teams, quotazioni, path, num_squadre, valori, fasce, fasce_goal, formazioni):
    rose = genera_rose(struttura_rosa, num_squadre)

    #voti_giornata is the imported dataframe which will be inserted in the loop
    all_points = pd.DataFrame(index = team_names)
    all_files = glob.glob(path + "/*.xlsx")
    i=1
    for filename in all_files:
        # this is to be read from file
        #print('Giornata attuale:' f'{i}\r', end="")
        i+=1
        voti_giornata = pd.read_excel(filename,sheet_name=0,skiprows=rows_to_skip)
        fixtures = fixture_gen(teams)
        dict_voti_giornata = all_grades_dict(struttura_rosa, quotazioni, voti_giornata, num_squadre)
        voti_squadre = voti_max(rose, struttura_rosa, formazioni, dict_voti_giornata, teams, num_squadre, valori, fasce)
        punti = pd.DataFrame.from_dict(points(fixtures, voti_squadre, fasce_goal),orient='index')
        all_points = pd.concat([all_points,punti],axis=1)
        #print(voti_squadre)
    total = pd.DataFrame(data= np.sum(np.array(all_points),axis=1,keepdims = True),  index=team_names, columns =['tot'])
    rose_id=rose
    rose = pd.DataFrame(data=rose, columns = team_names)
    rose_nomi = id_toName(struttura_rosa, quotazioni, rose, num_squadre, team_names)
    return [total, rose_nomi, rose_id]


# In[384]:


def main_model(n_campionati, struttura_rosa, team_names, teams, quotazioni, path, num_squadre = N_squadre, valori = Valori_modificatore, fasce = Fasce_modificatore, fasce_goal = Fasce_goal, formazioni = Formazioni):
    range_best = 100;
    q_range_best = 2000;
    for i in progressbar.progressbar(range(n_campionati)):
        #print('Campionato attuale:' f'{i+1}\r', end="")
        classifica, rose, rose_id= simula_campionato(struttura_rosa, team_names, teams, quotazioni, path, num_squadre, valori, fasce, fasce_goal, formazioni)
        quot_dict = all_quot_dict(struttura_rosa, quotazioni, num_squadre)
        classifica_quot = assign_quot(rose_id, quot_dict, team_names)
        range_temp = np.float(classifica.max() - classifica.min())
        q_range_temp = np.float(classifica_quot.max() - classifica_quot.min())
        if (range_temp < range_best + 10 and q_range_temp < q_range_best):
            range_best = range_temp
            q_range_best = q_range_temp
            classifica_best = classifica
            classifica_q_best = classifica_quot
            rose_best = rose
    return [rose_best, classifica_best, classifica_q_best]


# In[356]:

def styling_rows(x, struttura):
    [P,D,C,A] = struttura
    color_P = 'background-color: rgba(249,168,38,.5); color: black'
    color_D = 'background-color: rgba(46,125,51,.5); color: black'
    color_C = 'background-color: rgba(21,119,189,.5); color: black'
    color_A = 'background-color: rgba(198,40,39,.5); color: black'
    df_styler = pd.DataFrame('', index=x.index, columns=x.columns)
    col_idx = range(df_styler.shape[1])
    row_idx_P = P
    row_idx_D = D
    for idx in range(P):
        df_styler.iloc[idx, col_idx] = color_P
    for idx in range(P,P+D):
        df_styler.iloc[idx, col_idx] = color_D
    for idx in range(P+D,P+D+C):
        df_styler.iloc[idx, col_idx] = color_C
    for idx in range(P+D+C,P+D+C+A):
        df_styler.iloc[idx, col_idx] = color_A
    return df_styler

def ruoli(struttura_rosa):
    return struttura_rosa[0]*['P']+struttura_rosa[1]*['D']+struttura_rosa[2]*['C']+struttura_rosa[3]*['A']


# In[ ]:


def FC_colors(dataframe, struttura_rosa):
    output = dataframe.style.apply(styling_rows, struttura = struttura_rosa, axis = None)\
                .hide_index()
    return output