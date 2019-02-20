import json
import os
import requests
import pandas as pd
import time

def get_set_data(extra=False):
    #This is a method for getting the keys the keys in
    #pass in an arg to write the keys to Documents
    sets_json=get_json('https://api.scryfall.com/sets')
    set_name_lookup={}
    has_more=True
    while has_more:
        has_more=sets_json['has_more']
        for set_data in sets_json['data']:
            set_name_lookup[set_data['name']] = set_data['search_uri']
        if has_more:
            sets_json=get_json(sets_json['next_page'])
            temp_set_uri = sets_json['data'][0]['search_uri']
            temp_set=get_json(temp_set_uri)
    card_keys=list(temp_set['data'][0].keys())     
    if extra != False:
        user_path=os.path.expanduser("~/Documents")
        with open(user_path+"/keys.txt", 'w') as z:
            z.write("\n".join(card_keys))
    else:
        return card_keys,set_name_lookup
  

def get_json(url):
    time.sleep(.15)
    r=requests.get(url)
    if r.status_code != 200:
        pass
    else:
        return r.json()

def get_user_input(card_keys):
    #gets user input for which categories they want 
    '''
    user_responses=[]
    print("These are the various attributes you can write to the CSV")
    for key in card_keys:
        print(key)
    print("There is going to be a list of attributes printed. Hit return if you don't want that attribute recorded and anything else if you do")
    for key in card_keys:
        user_input=input(key)
        if user_input == '':
            continue
        else: 
            user_responses.append(key)'''
    return card_keys

def read_csv():
    #reads from desktop directory and pandas database
    user_path=os.path.expanduser("~/Desktop")
    csv_files=[]
    for file in os.listdir(user_path):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(user_path, file))

    for counter, file in enumerate(csv_files):
        print(file[(file.rfind('/')+1):] + ' [%d]' % (counter))
        counter+=1
    user_input=input("Which file do you want to use?")
    db=pd.read_csv(csv_files[int(user_input)])
    return db

def getAPI_set_data(set_url):
    card_data=[]
    has_more=True 
    #url='https://api.scryfall.com/cards/search?order=set&q=%2B%2Be%3A'
    while has_more==True:
        url_json=get_json(set_url)
        card_data+=url_json['data']
        has_more = url_json['has_more']
        if has_more:
            set_url=url_json['next_page']      
    return card_data
        
        
        
def fill_in_data(db,set_name_lookup,card_keys):
    user_input=get_user_input(card_keys)
    db=db.reindex(columns = db.columns.tolist()+user_input) #adds empty columns of user input to thing\
    for set_unique in (db.Set.unique()):
        try:        
            data_set=getAPI_set_data(set_name_lookup[set_unique])
            for index,card_row in db.loc[db['Set'] == set_unique].iterrows(): #generator object that returns all rows with certain set
                try:
                    temp_card_data = json_search(card_row['Name'],data_set)
                    fill_row(temp_card_data,db,index,user_input)                                                       
                except ValueError:
                    print("Check spelling of card: %s" % (card_row['Name']))
                    continue
        except KeyError:
            print("Check spelling of set: %s" % (set_unique))
            continue
    return db

def fill_row(temp_data,db,index,user_input):
    for option in user_input:
        db.loc[index,option] = temp_data[option]

def json_search(name,data_set):
    if '//' in name:
        name=name.split('//')[0] #Gatecrash // cards
    for card_name in data_set:
            if card_name['name'].strip().lower() == name.strip().lower():
                card_data = card_name
                break
    if isinstance(card_data, dict):
        return card_data
    else:
        raise ValueError
def main():
    db = read_csv()
    card_keys,set_name_lookup = get_set_data()
    db=fill_in_data(db,set_name_lookup,card_keys)
    db.to_csv("name_of_csv.csv")
    
    
    
if __name__=='__main__':
    main()
    
