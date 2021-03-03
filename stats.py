# retrieve stats on each player that has logged onto minecraft server

'''
    TODO:
    - create dataframe containing server stats
    - create dataframe containing player stats
        - total users w/ names -> usercache.json -> create cross ref. with UUID
        - grab all stats for each player from stats
        - grab all advancements / achievements from advancements
        - add in who is OP

    LONGTERM:
    - create minecraft story book from every message said in chat -> similar to group chat

    ?? .dat files ?? - what's in backpack ??
'''

import pandas as pd
from pandas import json_normalize
import json

def FlattenJson():
    test_dir = '/Users/lmiller/PythonProjects/MinecraftStats/proj/jsons/stats/0a1cef4e-ca8b-4392-9d82-5cd38a5e8c0a.json'
    with open(test_dir) as f:
        d = json.load(f)

    minestats = json_normalize(d['stats'])
    minestats.to_csv('/Users/lmiller/PythonProjects/MinecraftStats/proj/test.csv')


# will create csv from stats jsons and return csv
def CreateCSV(dir_to_usercache, dir_to_jsons):
    # imports usercache.json to df
    usercache = pd.read_json(dir_to_usercache)

    usercache_dict = {}

    stat_labels = [
                    'broken',
                    'crafted',
                    'custom',
                    'dropped',
                    'killed',
                    'killed_by',
                    'mined',
                    'picked_up',
                    'used']

    # creating a df for each user and uploading to Google Sheets
    for element in range(len(usercache.index)):

        # storing name in temp variable
        name = usercache.loc[:, 'name'][element]

        # adding each user stats as a df to a dictionary
        usercache_dict[element] = pd.read_json(dir_to_jsons + usercache.loc[:, 'uuid'][element] + '.json')

        # creating overall csv from each users dictionary
        #usercache_dict[element].to_csv('~/PythonProjects/MinecraftStats/proj/csvs/' + name + '.csv')

        # creating more detailed stats csv / user
        for stat in range(len(usercache_dict[element])):
            #
            detailed_stat = usercache_dict[element].loc[:, 'stats'][stat]

            # converting to json string
            stat_json = json.dumps(detailed_stat)

            # converting to df
            stat_df = pd.read_json(stat_json, typ='series')

            # converting to csv
            stat_df.to_csv('~/PythonProjects/MinecraftStats/proj/csvs/detailed_csvs/' + name + '-' + stat_labels[stat] + '.csv')


# will take outputted csv and upload to google sheets for all to view
def GoogleUpload(csv):
    pass

if __name__ == '__main__':
    dir_to_usercache = '~/PythonProjects/MinecraftStats/proj/jsons/usercache.json'
    dir_to_jsons = '~/PythonProjects/MinecraftStats/proj/jsons/stats/'
    CreateCSV(dir_to_usercache, dir_to_jsons)
    #FlattenJson()
