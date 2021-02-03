#!/usr/bin/env python
# coding: utf-8

# # FantAPPalla server
# 
# Documenting each of the functions in the server. So far I have completed up to 

# In[1]:


#Assigning this notebook as the server for the app

import anvil.server
from anvil import Image, XYPanel

anvil.server.connect("N2RJZAZY3RKJ65AUOA5JKOLC-GFGPDCRRTFT46NHQ")


# In[2]:


# Importing all the utilities
from utilities_stats import *
import copy

from anvil import URLMedia
import anvil.media
import datetime
from datetime import date
import time

from joblib import Parallel, delayed

#Setting the total number of matchdays in the season
tot_giornate = 35

# setting useful parameters
Teams, Logos, parameters, Results_0, goal_marks = set_par(fasce = 2)
giornate = current_matchday()

# filling individual dataframes and conditional display
Results = fill_dataframe_partita(Results_0, giornate, parameters, goal_marks, Teams, Print = False)

# saving cumulative statistical data
pf_med, pf_std, ps_med, ps_std, gf_med, gf_std = cumulative_data(Results, giornate, Print = False)

# Building cumulative dataframe
Total = make_Total_df(Results, giornate, goal_marks)
Tot_per_round = partial_totals(Results, giornate, tot_giornate, goal_marks)
#Total.head(10)


# In[3]:


#@anvil.server.callable
def current_matchDay():
    """
    Returns the current matchday, based on the local database of the matches data in the utilities python script.
    """
    return giornate


# In[4]:


#@anvil.server.callable
def generate_plots():
    """
    Generates all the plots for the IGnobel section and for the Cfactor section and saves them in a local folder.
    """
    
    giornate = current_matchday()
    Results = fill_dataframe_partita(Results_0, giornate, parameters, goal_marks, Teams, Print = False)

    for premio in ['Caduti','Porta Violata','Catenaccio','Panchina Oro','Cartellino Facile']:
        _ = premio_plot(Results, giornate, Teams, Logos, premio)
    fortuna_evo(Results, Teams, Tot_per_round)
    C_factor_logos_2(Total, giornate, Teams, tot_giornate, Logos)


# In[5]:


#generate_plots()


# In[6]:


# Imports all the libraries needed to manage the database
import json
from pymongo import MongoClient
from pprint import pprint
import pymongo

from datetime import datetime


with open('credential.json','r') as f:
    cred = json.load(f)
    

#creates the variables needed to manage the database
cluster = MongoClient(cred['cred'])
# choosing database
db = cluster["Game"]
# choosing collection
collection = db["Players"]
collection_man = db['Managers']
collection_tr = db['Transfers']

collection_temp = db["tempPlayers"]
collection_man_temp = db['tempManagers']
collection_tr_temp = db['tempTransfers']


# In[7]:


#@anvil.server.callable
def man_team_name(owner):
    """
    Given the owner of the team, fetches the name of the team from mongodb and returns it
    """
    
    owner = owner.lower()
    dic = collection_man.find_one({'owner': owner})
    
    return dic['team_name']


# In[8]:


#@anvil.server.callable

def rose_funct(owner, squad):
    """
    This is one of the most fundamental functions about a manager's lineup, it returns all possible information
    about the lineup, both contract players, including on loan, and loanee. Age, value, cost info etc.
    
    It is not called directly but it is used in another function to merge info about main and primavera.
    """
    
    
    flip_squad={
        'main':'primavera',
        'primavera':'main'
    }
    
    
    owner = owner.lower()
    squad = squad.lower()
    players = []
    
    value_init = 0
    value_now = 0
    
    
    mean_age = 0
    tot_cost = 0
    p_num_dict={
        'a contratto':0,
        'dentro in prestito':0,
        'fuori in prestito':0
    }
    
    posts = collection.find({'info.contract.owner': owner,'info.current_team.squad': squad})
    for player in posts:
        #check if loanee player comes from owner's squad 
        temp = ''
        if player['info']['current_team']['on_loan']:
            if squad not in player['info']['current_team']['previous_team']:
                continue
            else:
                p_num_dict['fuori in prestito'] +=1
                temp = '**'
            
        p_num_dict['a contratto'] +=1
        name_url = player['name']
        name_url = name_url.replace(' ','-')
        name_url = name_url.replace('.','')
        dag = ''
        cost_eff = player['info']['contract']['cost']
        if player['info']['personal_info']['team_real'] is None:
            stats_link = ''
            dag = '\u2020'
        else:
            stats_link = 'https://www.fantacalcio.it/squadre/'+player['info']['personal_info']['team_real']+'/'+name_url+'/'+str(player['_id'])
        
        age = int(np.floor((datetime.today()-datetime.strptime(player['info']['personal_info']['birthdate'], "%d/%m/%Y")).days/365.4))
        players.append({'role': player['info']['personal_info']['FC_role']
                        , 'name': player['name']
                        , 'age': age
                        , 'quotation': player['info']['stats']['Qt_A']
                        , 'quotation_initial': player['info']['contract']['quotation_initial']
                        , 'difference': int(player['info']['stats']['Qt_A']) - int(player['info']['current_team']['quotation_initial'])
                        , 'loan': temp+dag,
                       'link': stats_link,
                       'owner':owner,
                        'cost':cost_eff,
                       'complete_db': player})
        value_init += int(player['info']['contract']['quotation_initial'])
        value_now += int(player['info']['stats']['Qt_A'])
        mean_age += int(age)
        tot_cost += int(player['info']['contract']['cost'])
    
    posts = collection.find({'info.contract.owner': owner,'info.current_team.on_loan': True,'info.current_team.squad': flip_squad[squad]})
    for player in posts:
        #check if loanee player comes from owner's squad 
        temp = ''
        if player['info']['current_team']['on_loan']:
            if squad not in player['info']['current_team']['previous_team']:
                continue
            else:
                p_num_dict['fuori in prestito'] +=1
                temp = '**'
            
        p_num_dict['a contratto'] +=1
        name_url = player['name']
        name_url = name_url.replace(' ','-')
        name_url = name_url.replace('.','')
        dag = ''
        cost_eff = player['info']['contract']['cost']
        if player['info']['personal_info']['team_real'] is None:
            stats_link = ''
            dag = '\u2020'
        else:
            stats_link = 'https://www.fantacalcio.it/squadre/'+player['info']['personal_info']['team_real']+'/'+name_url+'/'+str(player['_id'])
        
        age = int(np.floor((datetime.today()-datetime.strptime(player['info']['personal_info']['birthdate'], "%d/%m/%Y")).days/365.4))
        players.append({'role': player['info']['personal_info']['FC_role']
                        , 'name': player['name']
                        , 'age': age
                        , 'quotation': player['info']['stats']['Qt_A']
                        , 'quotation_initial': player['info']['contract']['quotation_initial']
                        , 'difference': int(player['info']['stats']['Qt_A']) - int(player['info']['current_team']['quotation_initial'])
                        , 'loan': temp+dag,
                       'link': stats_link,
                       'owner':owner,
                        'cost':cost_eff,
                       'complete_db': player})
        value_init += int(player['info']['contract']['quotation_initial'])
        value_now += int(player['info']['stats']['Qt_A'])
        mean_age += int(age)
        tot_cost += int(player['info']['contract']['cost'])
    
    
    posts = collection.find({'info.current_team.owner': owner,'info.current_team.on_loan': True,'info.current_team.squad': squad})
    for player in posts:
        p_num_dict['dentro in prestito'] +=1
        temp = '*'
        name_url = player['name']
        name_url = name_url.replace(' ','-')
        name_url = name_url.replace('.','')
        dag = ''
        cost_eff = player['info']['current_team']['loan_info']['cost']
        if player['info']['personal_info']['team_real'] is None:
            stats_link = ''
            dag = '\u2020'
        else:
            stats_link = 'https://www.fantacalcio.it/squadre/'+player['info']['personal_info']['team_real']+'/'+name_url+'/'+str(player['_id'])
        
        age = int(np.floor((datetime.today()-datetime.strptime(player['info']['personal_info']['birthdate'], "%d/%m/%Y")).days/365.4))
        players.append({'role': player['info']['personal_info']['FC_role']
                        , 'name': player['name']
                        , 'age': age
                        , 'quotation': player['info']['stats']['Qt_A']
                        , 'quotation_initial': player['info']['current_team']['quotation_initial']
                        , 'difference': int(player['info']['stats']['Qt_A']) - int(player['info']['current_team']['quotation_initial'])
                        , 'loan': temp+dag,
                       'link': stats_link,
                       'owner':owner,
                        'cost':cost_eff,
                       'complete_db': player})
        value_init += int(player['info']['current_team']['quotation_initial'])
        value_now += int(player['info']['stats']['Qt_A'])
        mean_age += int(age)
        tot_cost += int(player['info']['contract']['cost'])
    
    mean_age = mean_age/len(players)
    return players, value_init, value_now, round(mean_age, 1), man_team_name(owner), tot_cost, p_num_dict


# In[9]:


@anvil.server.callable
def rose_funct_all(owner):
    """
    It uses the specific function rose_funct(owner, squad) to return information about the main and primavera
    squad of a given owner.
    
    Used by Form:
    - Squadra.Rosa
    """
    return rose_funct(owner, 'main'), rose_funct(owner, 'primavera')


# In[10]:


def count_prizes(palmares):
    """
    This is a support function used to count the prizes of each kind. It is given the palmares as it is in the 
    managers database on mongodb and it returns the overall number of trophies of each kind in a dictionary
    """
    
    
    sc=ch=cop=sup=tot=ig=pv=cf=po=ca=0
    for prize in palmares:
        if prize['Type'] == 'Coppa di Lega':
            cop+=1
        elif prize['Type'] == 'Scudetto':
            sc+=1
        elif prize['Type'] == 'Champions':
            ch+=1
        elif prize['Type'] == 'Supercoppa':
            sup+=1
        elif prize['Type'] == 'Porta Violata':
            pv +=1
        elif prize['Type'] == 'Cartellino Facile':
            cf +=1
        elif prize['Type'] == 'Panchina D\'Oro':
            po +=1
        elif prize['Type'] == 'Caduti':
            ca +=1
        ig=pv+cf+po+ca
        tot=cop+sc+ch+sup
    
    return {'tot': tot,'sc': sc, 'ch': ch, 'cop': cop, 'sup': sup, 'tot_ig': ig,'pv':pv, 'cf':cf, 'po':po, 'ca':ca}


# In[11]:


@anvil.server.callable

def man_data_tot(owner):
    """
    It returns a string with team_name and a dictionary with the details of a single owner. 
    Specifically it gives info about budgets, historic wins, 
    historic fines, current players overall cost (owned players, NOT received on loan). It also uses the function
    count_prizes to extract the total number of each trophy which was won in the history of the league. This
    function is called by several other functions in the server, as well directly by some forms.
    
    Used by Forms:
    - Squadra
    
    """
    
    owner = owner.lower()
    dic = collection_man.find_one({'owner': owner})
    team_name = dic['team_name']
    dic_out = {}
    
    dic_out['budget'] = dic['budget']
    dic_out['tot_wins'] = dic['total_wins']
    if len(dic['fines']):
        dic_out['tot_fines'] = pd.DataFrame(dic['fines']).Fine_eur.sum()
    else:
        dic_out['tot_fines'] = 0
    
    dic_out['tot_value'] = 0
    dic_out['tot_cost'] = 0
    for pl in collection.find({'info.contract.owner': owner}):
        dic_out['tot_value'] += int(pl['info']['stats']['Qt_A'])
        dic_out['tot_cost'] += int(pl['info']['contract']['cost'])
    
    dic_out['prizes'] = count_prizes(dic['palmares'])
    
    #card = anvil.media.from_file('Logos/'+owner+dic_res[res]+'.png','image/png')
    
    return dic_out, team_name


# In[12]:


@anvil.server.callable
def man_data_all():
    """
    It returns two dictionaries, with the number of trophies of each possible kind won by each owner in the history
    of the league. First dictionary if for league trophies, second id for ignobels.
    It uses the other function man_data_tot('owner') to fetch the individual owner's prize history.
    Used in the Forms:
    - Albo
    """
    
    dic_trophies = []
    dic_ig = []
    for owner in Teams.keys():
        dic_in, team_name = man_data_tot(owner)
        dic = {'team_logo_rep':owner,
            'team_name': team_name,
         'sc': dic_in['prizes']['sc'],
         'ch': dic_in['prizes']['ch'],
         'cop': dic_in['prizes']['cop'],
         'sup': dic_in['prizes']['sup'],
         'tot':dic_in['prizes']['tot']
         }
        dic_2 ={'team_logo_rep':owner,
            'team_name': team_name,
         'pv': dic_in['prizes']['pv'],
         'cf': dic_in['prizes']['cf'],
         'po': dic_in['prizes']['po'],
         'ca': dic_in['prizes']['ca'],
         'tot':dic_in['prizes']['tot_ig']
         }
        dic_trophies.append(dic)
        dic_ig.append(dic_2)
    return dic_trophies, dic_ig


# In[13]:


@anvil.server.callable
#cost is yet to fix

def finance_managers_data(SC = 360, LTL = 460): #SC and LTL will be determined from previous seasons, saved on mongoDB
    """
    This returns two list of dictionaries, used to fill repeating panels. It uses salary cap (SC) and luxury tax limit (LTL) as inputs. The dictionaries contain financial 
    information of all the owners on the database. The reason for the two lists is because of the form that calls this 
    function. It calls the function general_standing() to get the general standing, and inverts it to get the
    draft order, and the functino man_data_tot() for specific manager's details.
    Used by Forms:
    - Finanze
    """
    
    table_filler_1 = []
    table_filler_2 = []
    
    dict_standing = general_standing()
    
    for owner in Teams.keys():
        dict_out_1 = {}
        dict_out_2 = {}
        dic,  team_name = man_data_tot(owner)
        
        _, value_init_main, value_now_main, mean_age_main ,_, tot_cost_main,_ = rose_funct(owner, 'main')
        _, value_init_prima, value_now_prima, mean_age_prima ,_, tot_cost_main,_ = rose_funct(owner, 'primavera')
        
        dict_out_1['team'] = owner
        dict_out_2['team'] = owner
        
        dict_out_1['extra_budget'] = max(0, 100 + SC - int(value_now_main))
        dict_out_1['luxury_tax'] = max(0, int(value_now_main) - LTL)
        dict_out_1['budget'] = dic['budget']
        dict_out_1['draft_pick'] =  9 - int(dict_standing[owner])
        dict_out_2['trophies'] = dic['prizes']['tot']
        dict_out_2['trophies_ig'] = dic['prizes']['tot_ig']
        dict_out_2['tot_wins'] = dic['tot_wins']
        dict_out_2['tot_fines'] = dic['tot_fines']
        
        table_filler_1.append(dict_out_1)
        table_filler_2.append(dict_out_2)

    return table_filler_1, table_filler_2


# In[14]:


@anvil.server.callable
#cost is yet to fix

def finance_one_manager_data(owner, SC = 360, LTL = 460): #SC and LTL will be determined from previous seasons, saved on mongoDB
    """
    Uses owner, SC and LTL as inputs to return financial information about a given owner. It returns a dictionary with all
    the specific information.
    Used by Forms:
    - Squadra.Finanze
    
    """
    
    
    table_filler_1 = []
    
    dict_standing = general_standing()
    
    owner = owner.lower()
    dic = collection_man.find_one({'owner': owner})
    dic_2,  team_name = man_data_tot(owner)
    
    _, value_init_main, value_now_main, mean_age_main ,_, tot_cost_main,_= rose_funct(owner, 'main')
    _, value_init_prima, value_now_prima, mean_age_prima ,_, tot_cost_prima,_= rose_funct(owner, 'primavera')
    
    dic['extra_budget'] = max(0, 100 + SC - int(value_now_main))
    dic['luxury_tax'] = max(0, int(value_now_main) - LTL)
    dic['draft_pick'] = 9 - int(dict_standing[owner])
    dic['tot_fines'] = dic_2['tot_fines']
    dic['main_value'] = value_now_main
    dic['main_cost'] = value_now_main
    dic['prima_cost'] = value_now_main
    
    return dic
    
    


# In[15]:


@anvil.server.callable
#cost is yet to fix

def rose_managers_data(SC = 360, LTL = 460):
    
    """
    It takes salary cap (SC) and luxury tax limit (LTL) as input. It returns a list of dicionaries each with manager's 
    information about the lineup. It also returns a dictionary with the league medians.
    Used in Forms:
    - Rose
    """
    
    table_filler = []
    median_dict ={'Val_M':[],
                 'Val_P':[],
                 'Cost_M':[],
                 'Cost_P':[],
                 'Age_M':[],
                 'Age_P':[]}
    
    for owner in Teams.keys():
        dict_out = {}
        dic,  team_name = man_data_tot(owner)
        
        _, value_init_main, value_now_main, mean_age_main ,_,tot_cost_main, main_pl_num = rose_funct(owner, 'main')
        _, value_init_prima, value_now_prima, mean_age_prima ,_,tot_cost_prima, prima_pl_num= rose_funct(owner, 'primavera')
        
        dict_out['team'] = owner
        dict_out['extra_budget'] = max(0, 100 + SC - int(value_now_main))
        dict_out['luxury_tax'] = max(0, int(value_now_main) - LTL)
        dict_out['main_value'] = float(value_now_main)
        dict_out['prima_value'] = float(value_now_prima)
        dict_out['main_cost'] = float(tot_cost_main)
        dict_out['prima_cost'] = float(tot_cost_prima)
        dict_out['mean_age_main'] = float(mean_age_main)
        dict_out['mean_age_prima'] = float(mean_age_prima)
        #dict_out['draft_pick'] = 9 - int(dict_standing[owner])
        dict_out['trophies'] = int(dic['prizes']['tot'])
        dict_out['trophies_ig'] = int(dic['prizes']['tot_ig'])
        dict_out['tot_wins'] = int(dic['tot_wins'])
        dict_out['tot_fines'] = int(dic['tot_fines'])
        
        table_filler.append(dict_out)
        
        median_dict['Val_M'].append(float(value_now_main))
        median_dict['Val_P'].append(float(value_now_prima))
        median_dict['Age_M'].append(float(mean_age_main))
        median_dict['Age_P'].append(float(mean_age_prima))
        median_dict['Cost_M'].append(float(tot_cost_main))
        median_dict['Cost_P'].append(float(tot_cost_prima))
    
    median_dict['Val_M'] = float(np.median(median_dict['Val_M']))
    median_dict['Val_P'] = float(np.median(median_dict['Val_P']))
    median_dict['Age_M'] = float(np.median(median_dict['Age_M']))
    median_dict['Age_P'] = float(np.median(median_dict['Age_P']))
    median_dict['Cost_M'] = float(np.median(median_dict['Cost_M']))
    median_dict['Cost_P'] = float(np.median(median_dict['Cost_P']))
    
    
        
    return table_filler, median_dict


# In[16]:


@anvil.server.callable
def load_plot_C_all(regen = False):
    """
    It returns the current matchday, as well as two plots for Cfactor uploaded from the local folder 'Plots'.
    If regen = True, the function generate_plots() is called, that recreates these plots and saves them in the 
    same local folred, before uploading.
    Used in Forms:
    - Fortuna
    """
    
    if regen:
        generate_plots()
    card_hist = anvil.media.from_file('Plots/C_fact_'+ 'Historic' +'.png','image/png')
    card_tot = anvil.media.from_file('Plots/C_fact_'+ 'Total' +'.png','image/png')
    return giornate, card_tot, card_hist


# In[17]:


@anvil.server.callable
def load_IGNOBEL_db(plot):
    #tot = premio_plot(Results, giornate, Teams, Logos, plot)
    list_IG = sorted(dict_out[plot], key = lambda i: i['points'], reverse = True)
    i=1
    prize = 7 #to be determined via mongodb
    for el in list_IG:
        el['position'] = i
        el['team'] = el['team'].capitalize()
        el['prize'] = prize
        i+=1
    card = anvil.media.from_file('Plots/plot_'+ plot +'.png','image/png')
    #out_plot = load_plot_IG(plot)
    montepremi = str(4*prize) 
    return card, list_IG, giornate, montepremi


# In[18]:


def tot_fines():
    """
    Using the info extracted from man_data_owner(), it returns an updated dictionary with the total fines
    accumulated by each owner.
    It is called by other functions.
    """
    fines = 0
    for owner in Teams.keys():
        dic_man, _ = man_data_tot(owner)
        fines += dic_man['tot_fines']
    return fines


# In[19]:


@anvil.server.callable
def fetch_standing(standing):
    """
    For a given 'standing' parameter (points, goal etc), it returns the standing based on that parameter as a 
    list of dictionaries.
    It is called by other functions.
    """
    fines = tot_fines()
    posts = []
    for owner in Teams.keys():
        dic = Results[owner]
        points = dic[standing].sum() #without the sum, dic[standing] contains the progress, just in case one needs it for plotting live
        points_last = dic[standing][len(dic)]
        if standing in ['infortunati', 'cartellini', 'goal_subiti_por','bonus_panchina']:
            prize = 4 + fines/4 
        else:
            prize = None
        team = owner.capitalize()
        dic_0 = {
            'points':points,
            'points_last':points_last,
            'prize':prize,
            'team':team,
            'team_name': Teams[owner][0]
        }
        posts.append(dic_0)

    posts = sorted(posts, key = lambda i: i['points'], reverse = True)
    i=1
    for el in posts:
        el['position'] = i
        i+=1
    
    return posts, prize


# In[20]:


#@anvil.server.callable
def fetch_ALL_standings():
    """
    This returns the complete set of all the standings in the league, namely IGnobels and general/points. It is used 
    by other functions

    """
    
    dic_stand = {
        'Caduti': 'infortunati',
        'Cartellino Facile': 'cartellini',
        'Porta Violata': 'goal_subiti_por',
        'Catenaccio': 'mod_difesa',
        'Panchina Oro': 'bonus_panchina',
        'Generale': 'pti',
        'Avulsa': 'punti_fatti'
    }
    dic_out = {}
    for key, arg in dic_stand.items():
        posts, temp_prize = fetch_standing(arg)
        if temp_prize is not None:
            prize = temp_prize

        dic_out[key] = posts
    return dic_out, prize


# In[21]:


@anvil.server.callable
def fetch_Points_standings():
    """
    This returns the points-based standings in a two-keys dictionary.
    Used by Forms:
    - Stats

    """
    
    dic_stand = {
        'Generale': 'pti',
        'Avulsa': 'punti_fatti'
    }
    dic_out = {}
    for key, arg in dic_stand.items():
        posts, temp_prize = fetch_standing(arg)

        dic_out[key] = posts
    return dic_out


# In[22]:


#@anvil.server.callable
def fetch_IG_standings():
    """
    This returns the complete set of the IGnobel standings. It is called by other functions.
    
    """
    
    dic_stand = {
        'Caduti': 'infortunati',
        'Cartellino Facile': 'cartellini',
        'Porta Violata': 'goal_subiti_por',
        'Panchina Oro': 'bonus_panchina'
    }
    dic_out = {}
    for key, arg in dic_stand.items():
        posts, temp_prize = fetch_standing(arg)
        if temp_prize is not None:
            prize = temp_prize

        dic_out[key] = posts
    return dic_out, prize


# In[23]:


def general_standing():
    """
    It gives the general standing based on the current matchday. Note that it depends on the parameters that are
    imported at the beginning of the notebook, specifically Results, hence in order to refresh it needs to be run
    after Results is created from the utilities script.
    This is called by other functions.
    """
    
    posts,_ = fetch_standing('pti')
    dict_out={}
    for dic in posts:
        dict_out[dic['team'].lower()] = dic['position']
    return dict_out


# In[24]:


@anvil.server.callable
def load_IGNOBEL_db_all():
    """
    This returns a dictionary with the 4 lists corresponting to the standings for the ignobel prizes.
    also the current matchday and the overall money prize for the competitions. It uses the function
    fetch_IG_standings() to fetch the stats.
    Used by Forms:
    - Ignobel
    """
    
    list_IG, prize = fetch_IG_standings()
    montepremi_ig = 4*prize
    return list_IG, giornate, montepremi_ig


# In[25]:


@anvil.server.callable
def load_IGNOBEL_plots():
    """
    Returns dictionaries of the ignobel plots in anvil media format. It calls the function generate_plots() to 
    generate the plots and save them in the local folder Plot. Then it uploads them from there.
    Used by Forms:
    - Ignobel
    
    """
    
    plot_dict = {}
    generate_plots()
    time.sleep(3)
    for plot in ['Porta Violata', 'Cartellino Facile', 'Panchina Oro', 'Caduti']:
        plot_dict[plot] = anvil.media.from_file('Plots/plot_'+ plot +'.png','image/png')

    return plot_dict


# In[26]:


@anvil.server.callable
def all_players():
    """
    Returns the complete list of the names of all the players in the database.
    Used by the forms:
    - Admin_Transfers
    - Giocatori
    - Trasferimenti
    """
    
    
    down = list(collection.find({}))
    name_list = list(pd.DataFrame(down).name)
    return name_list


# In[27]:


def transfer_list(name):
    """
    Fetches all the transfers involving the player's name.
    """
    
    posts = list(collection_tr.find({'name':name}))
    return posts


# In[28]:


@anvil.server.callable
def full_pl_info(name):
    """
    Returns the player's info, including the full dictionary, the URL media from the link from fc.it, the link to the 
    statistics from FC and the list of all the transfers in which the player was involved.
    To fetch the transfers the function transfer_list(name) is used.
    Used by Forms:
    - Giocatori_lower
    
    """
    
    dic = collection.find_one({'name': name})
    
    name_url = dic['name']
    name_url = name_url.replace(' ','-')
    name_url = name_url.replace('.','')
    
    age = date.today().year - int(dic['info']['personal_info']['birthdate'][6:10])
    dic['info']['personal_info']['age']= ' ('+ str(age)+')'
    
    card = URLMedia('https://content.fantacalcio.it/web/campioncini/card/'+name_url+'.jpg')
    
    if dic['info']['personal_info']['team_real'] is None:
        stats_link = ''
    else:
        stats_link = 'https://www.fantacalcio.it/squadre/'+dic['info']['personal_info']['team_real']+'/'+name_url+'/'+str(dic['_id'])
    
    return dic, card, stats_link, transfer_list(name)


# In[29]:


@anvil.server.callable
def save_transfer_mongo(dic, player = False, loan_info = False):
    """
    It is used to make modifications directly to the databases of transfers and players. It takes all the parameters that are
    inserted from the app and directly creates/overwrites the entries in the database.
    Used by the Forms:
    - Admin_Transfers
    """
    
    now = datetime.today()
    Id = now.strftime("%Y%m%d%H%M%S")
    
    
    res = dic
    res['_id'] = Id
    
    if loan_info:
        date_now = date.today()
        m, y = date_now.month, date_now.year
        if m > 7:
            y = y + 1
        
        loan_info['expire_date'] = str(y)+'/07/31'
        res['loan_info'] = loan_info
    
    
        
        
    
    collection_tr.insert_one(res)
    
    if player:
        if dic['operation'] in ['Asta', 'Draft', 'Acquisto', 'Scambio', 'Algoritmo', 'Svincolo']:
            cost_exch = 0
            if dic['operation'] == 'Scambio':
                dic_exch = collection.find_one({'name': dic['exchange_player']})
                cost_exch = int(dic_exch['info']['contract']['cost'])
                
            collection.update_one({'name':dic['name']},{'$set':{'info.contract.start_date':dic['date']}})
            collection.update_one({'name':dic['name']},{'$set':{'info.contract.cost':int(dic['cost']) + cost_exch}})
            collection.update_one({'name':dic['name']},{'$set':{'info.contract.acquisition_mode':dic['operation']}})
            collection.update_one({'name':dic['name']},{'$set':{'info.contract.previous_owner':dic['previous_owner']}})
            collection.update_one({'name':dic['name']},{'$set':{'info.contract.quotation_initial':int(dic['quotation_to_date'])}})
        
        if loan_info:
            collection.update_one({'name':dic['name']},{'$set':{'info.current_team.on_loan':True}})
            collection.update_one({'name':dic['name']},{'$set':{'info.current_team.loan_info':loan_info}})
        
        
        collection.update_one({'name':dic['name']},{'$set':{'info.current_team.start_date':dic['date']}})
        collection.update_one({'name':dic['name']},{'$set':{'info.current_team.owner':dic['new_owner']}})
        collection.update_one({'name':dic['name']},{'$set':{'info.current_team.squad':dic['squad']}})
        if dic['previous_owner'] is None:
            previous_team = None
        else:
            previous_team = dic['previous_owner']+', '+dic['previous_squad']
        collection.update_one({'name':dic['name']},{'$set':{'info.current_team.previous_team':previous_team}})
        collection.update_one({'name':dic['name']},{'$set':{'info.current_team.quotation_initial':int(dic['quotation_to_date'])}})
    
    dic_tr = collection_tr.find_one({'_id':Id})
    dic_pl = 'Non Aggiornato'
    if player:
        dic_pl = collection.find_one({'name':dic['name']})
    
    
    return str(dic_tr), str(dic_pl)


    


# In[30]:


@anvil.server.callable
def all_flags_list():
    """
    It returns the flags of all the nationalities of the players on mongodb in anvil media format. It would give error if 
    some file is missing, in that case it needs to be downloaded and saved in the folder 'Bandiere' in png format.
    Used in the Forms:
    - Admin_area
    
    """
    
    posts = collection.find({})

    all_pl = []
    for pl in posts:
        if 'personal_info' in pl['info'].keys():
            all_pl.append(pl['info']['personal_info']['nation'])

    nations = []
    for nat in all_pl:
        if ',' in nat:
            nat_2 = nat.split(', ')
            nations.append(nat_2[0].lower())
            nations.append(nat_2[1].lower())
        else:
            nations.append(nat.lower())


    dict_flag = {}#[{'res':'high'}]
    for nat in nations:
        dict_flag[nat] = anvil.media.from_file('../Bandiere/'+ nat +'.png','image/png')
    return dict_flag


# In[31]:


@anvil.server.callable
def all_team_logos_list():
    """
    It returns the logos of all the real teams of the players on mongodb in anvil media format. It would give error if 
    some file is missing, in that case it needs to be downloaded and saved in the folder 'Scudetti' in png format.
    Used in the Forms:
    - Admin_area
    
    """
    
    posts = collection.find({})

    all_pl = []
    for pl in posts:
        if 'personal_info' in pl['info'].keys():
            if pl['info']['personal_info']['team_real'] is None:
                all_pl.append('svincolato')
            else:
                all_pl.append(pl['info']['personal_info']['team_real'])

    teams = []
    for team in all_pl:
        teams.append(team.lower())


    dict_logos = {}#[{'res':'high'}]
    for team in teams:
        dict_logos[team] = anvil.media.from_file('../Scudetti/'+ team +'.png','image/png')
    return dict_logos


# In[32]:


@anvil.server.callable
def fetch_transfers(dic):
    """
    This returns a list of dictionaries straight from the transfer database that match the filters included 
    in the dictionary dic used as input.
    Used by Forms:
    - Trasferimenti
    """
    
    
    
    filt = {}
    from_owners = []
    for el in dic['from_list']:
        if el['checked']:
            from_owners.append(el['owner'])
    filt['previous_owner'] = {'$in': from_owners}
    
    
    to_owners = []
    for el in dic['to_list']:
        if el['checked']:
            to_owners.append(el['owner'])
    filt['new_owner'] = {'$in': to_owners}
    
    operations = []
    for el in dic['operations']:
        if el['checked']:
            operations.append(el['operation'])
    filt['operation'] = {'$in': operations}
    
    
    if dic['from_squad']['main']:
        filt['previous_squad'] = 'main'
    elif dic['from_squad']['primavera']:
        filt['previous_squad'] = 'primavera'
    
    if dic['to_squad']['main']:
        filt['squad'] = 'main'
    elif dic['to_squad']['primavera']:
        filt['squad'] = 'primavera'
    
    if dic['name'] is not None:
        filt['name'] = dic['name']
    
    Min = -100
    Max = 1000
    
    if dic['cost']['min'] is not None:
        Min = dic['cost']['min']
    if dic['cost']['max'] is not None:
        Max = dic['cost']['max']
    
    filt['cost'] = {'$gte':int(Min), '$lte':int(Max)}
    
    date_Min = 0
    date_Max = 10**10
    
    if dic['dates']['from'] is not None:
        date_Min = int(dic['dates']['from'].strftime('%Y%m%d'))
    if dic['dates']['to'] is not None:
        date_Max = int(dic['dates']['to'].strftime('%Y%m%d'))
    
    filt['date_num'] = {'$gte':int(date_Min), '$lte':int(date_Max)}
    
    
                
    #dic['dates'] 
    
    print(filt)
    output = list(collection_tr.find(filt))
    
    return output


# In[33]:


@anvil.server.callable
def fetch_teams_real(checked = True):
    """
    It returns a list of dictionaries with all the real teams' names in the database.
    Used by Forms:
    - Giocatori
    """
    
    posts = collection.find()
    teams_dict = []
    teams = []
    for pl in posts:
        team_real = filter_team =  pl['info']['personal_info']['team_real']
        if team_real is None:
            continue #team_real = 'Non in Serie A'
        if team_real not in teams:
            teams_dict.append({'filter_team': filter_team,'team_name': team_real, 'checked': checked})
            teams.append(team_real)
    return teams_dict + [{'filter_team': None,'team_name': 'Non in Serie A', 'checked': True}]


# In[34]:


@anvil.server.callable
def fetch_players_database(dic):
    """
    Given an input from the appropriate filters as dictionary, it returns the list of dictionaries of the corresponding
    players from mongodb.
    Used in Forms:
    - Giocatori
    """
    
    filt = {}
    owners = []
    for el in dic['owners']:
        if el['checked']:
            owners.append(el['owner'])
    filt['info.contract.owner'] = {'$in': owners}
    
    if dic['squad']['main'] ^ dic['squad']['primavera']:
        if dic['squad']['main']:
            filt['info.current_team.squad'] = 'main'
        elif dic['squad']['primavera']:
            filt['info.current_team.squad'] = 'primavera'
    if dic['squad']['loan']:
        filt['info.current_team.on_loan'] = True
    
    
    roles = []
    for el in dic['roles']:
        if el['checked']:
            roles.append(el['role'])
    filt['info.personal_info.FC_role'] = {'$in': roles}
    
    
    Min_q = dic['quot']['min']
    Max_q = dic['quot']['max']
    
    filt['info.stats.Qt_A'] = {'$gte':int(Min_q), '$lte':int(Max_q)}
    
    Min_birth = int(date.today().strftime('%Y%m%d'))-dic['age']['min']*10**4
    Max_birth = int(date.today().strftime('%Y%m%d'))-dic['age']['max']*10**4
    
    filt['info.personal_info.birthdate_num'] = {'$lte':int(Min_birth), '$gte':int(Max_birth)}#inversed of course
    
    teams_real = []
    for el in dic['teams_real']:
        if el['checked']:
            teams_real.append(el['filter_team'])
    filt['info.personal_info.team_real'] = {'$in': teams_real}
    
    posts = list(collection.find(filt))
    
    return posts


# In[37]:


######################################################################
# Dictionary for form: Squadra.Stats
######################################################################
def score_label(df, giornata):
    return '%d-%d' % (df.at[giornata,'GF'], df.at[giornata,'GS'])

def best_worst_games(df):
    '''Returns two dictionaries: best win and worst loss in Campionato'''    
    df['scarto_goal'] = df['GF'] - df['GS']
    df['scarto_fp'] = df['punti_fatti'] - df['punti_subiti']
    giornata_best_win = df['scarto_goal'].idxmax()
    best_win = {
        'giornata': giornata_best_win,
        'score': '%d-%d' % (df.at[giornata_best_win,'GF'], df.at[giornata_best_win,'GS']),
        'avversario': df.at[giornata_best_win,'avversario']
    }
    giornata_worst_loss = df['scarto_goal'].idxmin()
    worst_loss = {
        'giornata': giornata_worst_loss,
        'score': '%d-%d' % (df.at[giornata_worst_loss,'GF'], df.at[giornata_worst_loss,'GS']),
        'avversario': df.at[giornata_worst_loss,'avversario']
    }
    return best_win, worst_loss

def scontri_diretti(df, avversario):
    '''Returns a disctionary with results against an opponent'''
    df = df[df['avversario'] == avversario]
    punti = df['pti'].sum()
    media_punti = punti/len(df)
    wins = len(df[df['esito'] == 'V'])
    draws = len(df[df['esito'] == 'P'])
    losses = len(df[df['esito'] == 'S'])
    dic = {'avversario': avversario, 'vittorie': wins, 'pareggi': draws, 'sconfitte': losses}
    best_win, worst_loss = best_worst_games(df)
    dic['best_win'] = best_win
    dic['worst_loss'] = worst_loss
    dic['media_punti'] = media_punti
    return dic

def get_matchday_dict(df, giornata):
    '''Returns a disctionary with info about a matchday of a given team'''
    dic = {}
    dic['giornata'] = giornata
    dic['avversario'] = df.at[giornata, 'avversario']
    dic['score'] = score_label(df, giornata)
    dic['GF'] = df.at[giornata, 'GF']
    dic['GS'] = df.at[giornata, 'GS']
    dic['fantapunti_fatti'] = df.at[giornata, 'punti_fatti']
    dic['fantapunti_subiti'] = df.at[giornata, 'punti_subiti']
    dic['esito'] = df.at[giornata, 'esito']
    return dic

def results_arr(df):
    '''Returns a disctionary with results of a team'''
    results_array = []
    for giornata in range(1, len(df)+1):
        dic = get_matchday_dict(df, giornata)
        results_array.append(dic)
    return results_array

def get_close_games_dict(df, threshold = 2, verbose=False):
    '''Returns a disctionary with results of a team of close_games'''
    giornate = len(df)
    
    close_games_dict = {}
    close_games_arr = []
    pti = 0
    n_close_games = 0
    
    for gg in df.index:     
        if (np.abs(df['punti_fatti'][gg] - df['punti_subiti'][gg])) <= threshold:
            matchday_dict = get_matchday_dict(df, gg)
            close_games_arr.append(matchday_dict)
            
            res = esito(df.GF[gg], df.GS[gg])
            if verbose:                
                print('G', gg, '| punti fatti:', df.punti_fatti[gg], ' ( subiti:', df.punti_subiti[gg],') |', res, '(', df.GF[gg], '-', df.GS[gg], ')')
            pti = pti+punti(res)
            n_close_games = n_close_games + 1
    
    if n_close_games > 0:
        if verbose: print('---> %d punti in %d giornate \n     (media: %.2f)' % (pti, n_close_games, pti/n_close_games))
        close_games_dict['punti'] = pti
        close_games_dict['n_close_games'] = n_close_games
        close_games_dict['media_punti'] = float(pti) / n_close_games
    else:
        if verbose: print('---> No close games found')
        close_games_dict['punti'] = pti
        close_games_dict['n_close_games'] = n_close_games
        close_games_dict['media_punti'] = float(pti) / n_close_games
    
    close_games_dict['games_list'] = close_games_arr
    return close_games_dict

    
def team_stats_dict(owner):
    '''Builds a nested dictionary with stats in Campionato per team'''
    #stats_dict = {}
    df = Results[owner]

    team_stats_dict = {}
    team_stats_dict['media_fantapunti_fatti'] = np.mean(df['punti_fatti'])
    team_stats_dict['media_fantapunti_subiti'] = np.mean(df['punti_subiti'])
    team_stats_dict['media_GF'] = np.mean(df['GF'])
    team_stats_dict['media_GS'] = np.mean(df['GS'])
    team_stats_dict['media_punti'] = np.mean(df['pti'])

    team_stats_dict['max_fantapunti'] = max(df['punti_fatti'])
    team_stats_dict['min_fantapunti'] = min(df['punti_fatti'])

    best_win, worst_loss = best_worst_games(df)
    team_stats_dict['best_win'] = best_win
    team_stats_dict['worst_loss'] = worst_loss

    team_stats_dict['results'] = results_arr(df)
    
    team_stats_dict['close_games'] = get_close_games_dict(df)

    team_stats_dict['scontri_diretti'] = []
    for avv in df['avversario'].unique():
        team_stats_dict['scontri_diretti'].append(scontri_diretti(df, avv))

    return team_stats_dict


# Anvil server function
@anvil.server.callable
def team_stats(owner):
    """
    Returns a dictionary with several info about team stats in Campionato
    """
    dic = team_stats_dict(owner)
    return dic


# In[41]:





# In[ ]:




