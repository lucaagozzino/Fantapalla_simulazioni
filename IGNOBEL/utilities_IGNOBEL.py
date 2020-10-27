from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
import progressbar

options = Options()
options.headless = True
options.add_argument("--window-size=1920,10200") #this is important, to tell it how much of the webpage to import
driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')

#rivedere i vari xpath, nel caso in cui la struttura del sito e' diversa

def formazioni(competizione = 'campionato'):
    #if competizione == 'campionato':
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni?id=185855'
    driver.get(link)

    players = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text


            all_playersE = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@class='player-list-item even  ']/td[1]/span/span[2]/a")
            all_playersO = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@class='player-list-item odd  ']/td[1]/span/span[2]/a")
            all_playersEP = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item even  ']/td[1]/span/span[2]/a")
            all_playersOP = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item odd  ']/td[1]/span/span[2]/a")
            #all_playersE = driver.find_elements_by_xpath("")

            all_pl = all_playersE + all_playersO + all_playersEP + all_playersOP
            names = []
            for pl in all_pl:
                names.append((pl.text).upper())
            players[name] = names
    return pd.DataFrame.from_dict(data=players, orient='index').T

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#def infortunati(link = 'https://www.pianetafanta.it/Giocatori-Infortunati.asp'):

#    driver.get(link)
#    names = driver.find_elements_by_xpath("//*[@id='my_id_div']/div[6]/div[11]/div[2]/div/div[@class]/div/table/tbody/tr[@class]/td[2]/a/strong")

#    players = []
#    for n in names:
#        players.append(n.text.upper())

#    return players

def infortunati(giornata):
    link = 'https://www.fantacalcio.it/cartella-medica/'+str(giornata+3)#adjusted for our start of the season
    driver.get(link)
    button = driver.find_element_by_id("tabAll")

    driver.execute_script("arguments[0].click();", button)

    test = driver.find_elements_by_xpath("/html/body/div[7]/div[5]/main/div/div/div/div[1]/div[2]/div[5]/div[@class]/div/div/div[2]/div/div[1]/p[@class]/span")
    all_inf = []
    for pl in test:
        all_inf.append(pl.text)
    return all_inf

def rose(link = 'https://leghe.fantacalcio.it/fantapalla-forever/area-gioco/rose?id=185855'):
    
    driver.get(link)
    rose = {}


    for j in range(1,9):
        test_1 = []
        name = (driver.find_element_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li['+str(j)+']/div/div[1]/div[2]/h4').text).upper()
        players = driver.find_elements_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li['+str(j)+']/table/tbody/tr[@class]/td[2]/a/b')
        for pl in players:
            test_1.append((pl.text).upper())

        rose[name] = test_1
        
        
    return pd.DataFrame.from_dict(data=rose, orient='index').T

def count_inf(I , R ):
    count = {}

    all_names = ''.join(I)
    for team in R:
        c = 0
        for player in R[team]:
            if player == None:
                continue
            if player in ''.join(I):
                c+=1
        count[team] = c
    return pd.DataFrame(data = count, index = ['tot Infortunati'])

def bonus_panchina(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)
    driver.get(link)

    all_voti = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            #name = driver.find_element_by_xpath("/html/body/div[12]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text
            Fvoto_o = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class = 'player-list-item odd  ']/td[5]/span")
            Nvoto_o = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class = 'player-list-item odd  ']/td[4]/span")
            Fvoto_e = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class = 'player-list-item even  ']/td[5]/span")
            Nvoto_e = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class = 'player-list-item even  ']/td[4]/span")
            Fvoti = Fvoto_o + Fvoto_e
            Nvoti = Nvoto_o + Nvoto_e
            tot = []
            for i in range(len(Fvoti)):
                if Fvoti[i].text != '-':
                    tot.append(max(0,float(Fvoti[i].text)-float(Nvoti[i].text)))
            all_voti[name] = [sum(tot)]
    return pd.DataFrame(data=all_voti,index = ['Bonus Panchinari'])


def goal_subiti(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)
    driver.get(link)

    all_goal = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            if len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@class='player-list-item even  out']/td[@class='cell-text cell-primary x7 smart-x9 smart-role role-p']")) == 0:

                goal = len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[1]/td[3]/ul/li[@data-original-title='Gol subito (-0.5)']"))
            else:
                goal1 = len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item even in ']/td[3]/ul/li[@data-original-title='Gol subito (-0.5)']"))
                goal2 = len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item odd in ']/td[3]/ul/li[@data-original-title='Gol subito (-0.5)']"))
                goal = max(goal1,goal2)
            all_goal[name] = goal

    return pd.DataFrame(data=all_goal,index = ['Goal subiti'])


def modificatore(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)
    driver.get(link)

    all_mod = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            all_mod[name] = 0
            temp = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[3]/tbody/tr/td[1]/span")
            if len(temp)>0 and temp[0].text == 'Modificatore Difesa':
                mod = float(driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[3]/tbody/tr/td[2]/span").text)
                all_mod[name] = float(mod)
    return pd.DataFrame(data=all_mod, index = ['Modificatore'])


def scarica_voti(giornata, stagione ='2020-21'):
    data = pd.read_excel('http://www.fantacalcio.it/Servizi/Excel.ashx?type=1&g='+str(giornata)+'&t=1601872625000&s='+stagione,skiprows = [0,1,2,3,4])
    data = data[data.Nome != 'Nome']
    data = data.dropna()
    data.index = list(range(len(data)))
    return data

def cartellini(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)
    driver.get(link)

    all_cart = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            gialli = len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@data-id]/td[3]/ul/li[@data-original-title='Ammonizione (-0.25)']"))
            gialliPE= len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item even in ']/td[3]/ul/li[@data-original-title='Ammonizione (-0.25)']"))
            gialliPO= len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item odd in ']/td[3]/ul/li[@data-original-title='Ammonizione (-0.25)']"))
            rossi =  len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@data-id]/td[3]/ul/li[@data-original-title='Espulso (-0.5)']"))
            rossiPE=len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item even in ']/td[3]/ul/li[@data-original-title='Espulso (-0.5)']"))
            rossiPO=len(driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item odd in ']/td[3]/ul/li[@data-original-title='Espulso (-0.5)']"))
            all_cart[name] = [gialli+gialliPE+gialliPO, rossi]
    return pd.DataFrame(data=all_cart,index = ['C. gialli','C. rossi'])

def fantapunti_subiti(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)
    driver.get(link)

    all_punti = {}
    for l in [2,3,4,5]:
        name={}
        punti={}
        for k in [1,2]:
            name[k] = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            punti[k] = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[4]/tfoot/tr/td[2]/div").text[:-7]
        all_punti[name[1]]=float(punti[2])
        all_punti[name[2]]=float(punti[1])
            
    return pd.DataFrame(data=all_punti,index = ['Fantapunti Subiti'])  

def fantapunti_fatti(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)
    driver.get(link)

    all_punti = {}
    for l in [2,3,4,5]:
        name={}
        punti={}
        for k in [1,2]:
            name[k] = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            punti[k] = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[4]/tfoot/tr/td[2]/div").text[:-7]
        all_punti[name[1]]=float(punti[1])
        all_punti[name[2]]=float(punti[2])
            
    return pd.DataFrame(data=all_punti,index = ['Fantapunti Fatti'])

def IGNOBEL_tot(giornata):
    V = bonus_panchina(giornata) 
    G = goal_subiti(giornata)
    M = modificatore(giornata) 
    C = cartellini(giornata)
    CI = count_inf(infortunati(giornata), rose())
    F = fantapunti_fatti(giornata)
    S = fantapunti_subiti(giornata)
    output = pd.concat([F,S,G,C,V,M,CI], axis = 0).T
    output = output.astype({"tot Infortunati": int,"Goal subiti": int, "Modificatore": int,"C. gialli": int,"C. rossi": int}) 
    return output.T

def storico_IG(giornata, dict_names, path = "Dati_storici/"):

    test_dict={
        'enzo':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'pietro':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'mario':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'musci8':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'franky':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'nanni':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'emiliano':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'luca':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']}}
    for i in range(1,giornata+1):
        G=pd.read_pickle(path+"Giornata_"+str(i)+".pkl")
        for team, content in G.items():
            test_dict[dict_names[team]][i] = [i, content[0], float(content[1]), content[2], content[3]+2*content[4], content[5], content[6], content[7], dict_names[team]]
    return(test_dict)

def storico_individuale(nome, giornata):
    dict_names={
    'AS 800A': 'enzo',
    'PDG 1908': 'pietro',
    'IGNORANZA EVERYWHERE': 'mario',
    'SOROS FC': 'musci8',
    'MAINZ NA GIOIA': 'franky',
    'PALLA PAZZA': 'nanni',
    'I DISEREDATI': 'emiliano',
    'XYZ': 'luca'
    }

    test_dict = storico_IG(giornata, dict_names)
    
    df = pd.DataFrame(data=test_dict[nome]).T
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header
    #df = df.reset_index()
    #df = df.drop('index',axis=1)
    return df

def aggiorna_database(giornata):
    nomi=[
        'enzo',
        'pietro',
        'mario',
        'musci8',
        'franky',
        'nanni',
        'emiliano',
        'luca'
    ]
    for name in nomi:
        df = storico_individuale(name, giornata)
        df.to_pickle("Dati_individuali/"+ name +".pkl")
    print("Dati aggiornati fino alla "+str(giornata)+" giornata")