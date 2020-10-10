from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.common.exceptions import NoSuchElementException        

options = Options()
options.headless = True
options.add_argument("--window-size=1920,10200") #this is important, to tell it how much of the webpage to import
driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')

#rivedere i vari xpath, nel caso in cui la struttura del sito e' diversa

def formazioni(link = 'https://leghe.fantacalcio.it/fantapalla/formazioni'):#'https://leghe.fantacalcio.it/fantapalla-forever/formazioni'):
    
    #sample_link'https://leghe.fantacalcio.it/fantapalla/formazioni'
    driver.get(link)
    formazioni = {}
    
    for l in [2,3,4,5]:
        for k in [1,2]:
            temp = []
            for i in range(1,12):
                test = driver.find_element_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div['+str(l)+']/div[2]/div['+str(k)+']/table[1]/tbody/tr['+str(i)+']/td[1]/span/span[2]/a')
                team_name = driver.find_element_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div['+str(l)+']/div[1]/div['+str(k)+']/div/div[2]/h4')
                temp.append(test.text)
            for j in range(1,8):
                test = driver.find_element_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div['+str(l)+']/div[2]/div['+str(k)+']/table[2]/tbody/tr['+str(j)+']/td[1]/span/span[2]/a')
                #test = driver.find_element_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div[2]/table[2]/tbody/tr['+str(j)+']/td[1]/span/span[2]/a')
                temp.append(test.text)
            formazioni[team_name.text]= temp
            
    return pd.DataFrame(data=formazioni)

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def infortunati(link = 'https://www.pianetafanta.it/Giocatori-Infortunati.asp'):

    driver.get(link)

    test={}

    j=3
    while True:
        if check_exists_by_xpath('//*[@id="my_id_div"]/div[6]/div[11]/div[2]/div/div['+str(j)+']/div/div[1]/h3/strong'):
            team = (driver.find_element_by_xpath('//*[@id="my_id_div"]/div[6]/div[11]/div[2]/div/div['+str(j)+']/div/div[1]/h3/strong').text).upper()
        else:
            break
        temp=[]
        i=2
        while True:
            if check_exists_by_xpath('//*[@id="my_id_div"]/div[6]/div[11]/div[2]/div/div['+str(j)+']/div/table/tbody/tr['+ str(i) +']/td[2]/a/strong'):
                temp.append((driver.find_element_by_xpath('//*[@id="my_id_div"]/div[6]/div[11]/div[2]/div/div['+str(j)+']/div/table/tbody/tr['+ str(i) +']/td[2]/a/strong').text).upper())
                i += 1
            else: 
                break
        j += 1
        test[team] = temp

    infortunati = pd.DataFrame.from_dict(data=test, orient='index').T

    return infortunati

def rose(link = 'https://leghe.fantacalcio.it/fantapalla-forever/area-gioco/rose'):
    
    driver.get(link)
    rose = {}


    for j in range(1,9):
        test_1 = []
        name = (driver.find_element_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li['+str(j)+']/div/div[1]/div[2]/h4').text).upper()
        for i in range(1,26):
            temp_1 = driver.find_element_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li['+str(j)+']/table/tbody/tr['+str(i)+']/td[2]/a/b')
            #test_2 = driver.find_element_by_xpath('/html/body/div[7]/main/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li[1]/table/tbody/tr[2]/td[2]/a/b')
            test_1.append((temp_1.text).upper())
        rose[name] = test_1
        
        
    return pd.DataFrame(data=rose)

def count(I = infortunati(), R = rose()):
    count_inf = {}
    test = list(filter(None,I.values.flatten()))
    separator = ','
    all_names = separator.join(test)
    for team in R:
        c = []
        for player in R[team]:
            c.append(player in all_names)
        count_inf[team] = sum(c)
    return pd.DataFrame(data = count_inf, index = ['N. Inf.'])