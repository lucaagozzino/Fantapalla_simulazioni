import pandas as pd

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