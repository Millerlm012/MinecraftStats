# retrieve stats on each player that has logged onto minecraft server

'''
    TODO / Future Add On's:
    - add in player achievements
    ?? .dat files ?? - what's in backpack ??

    LONGTERM:
    - create minecraft story book from every message said in chat -> similar to SMS group chat
'''

import pandas as pd
from pandas import json_normalize
import os
import time
import json
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery


# will create csv from stats jsons and return csv -> prep work before upload
def CreateCSV(dir_to_usercache, dir_to_jsons):
    # imports usercache.json to df
    usercache = pd.read_json(dir_to_usercache)

    usercache_dict = {}

    # creating a df for each user and uploading to Google Sheets
    for element in range(len(usercache.index)):

        # storing name for easy later acess
        name = usercache.loc[:, 'name'][element]

        # adding each user stats as a df to a dictionary
        usercache_dict[element] = pd.read_json(dir_to_jsons + usercache.loc[:, 'uuid'][element] + '.json')

        # creating more detailed stats csv for each user
        for stat in range(len(usercache_dict[element])):
            detailed_stat = usercache_dict[element].loc[:, 'stats'][stat]

            # converting to json string
            stat_json = json.dumps(detailed_stat)

            # converting to df
            stat_df = pd.read_json(stat_json, typ='series')

            # renaming index and columns
            stat_df.index.names = ['Type:']

            # storing name of what the csv will be named
            name_csv = name + '-' + usercache_dict[element].index[stat] + '.csv'

            # converting to csv
            stat_df.to_csv('~/PythonProjects/MinecraftStats/proj/csvs/detailed_csvs/' + name_csv)

            print('Attempting to open stats spreadsheet for...', name)

            # processing the upload to google
            GoogleUpload(name_csv, name)

################################################################################
# will take outputted csv and upload to google sheets for all to view
def GoogleUpload(name_csv, name):

    # changing directory to where json is stored
    os.chdir('/Users/lmiller/PythonProjects/MinecraftStats/')

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Minecraft-Stats-80f246126602.json', scope)
    client = gspread.authorize(creds)

    # authorize creds
    gc = gspread.authorize(creds)

    # changing directory back to proj directory
    os.chdir('/Users/lmiller/PythonProjects/MinecraftStats/proj')

    # csv directory
    csvFile = '/Users/lmiller/PythonProjects/MinecraftStats/proj/csvs/detailed_csvs/' + name_csv

    # creating google drive destination folder for spreadsheet
    dest_folder_id = '1UvIpaqRWbxj5ueEG6IUfeqS-iKppU9t3'


    ############################################################################
    # attempting to open user spreadsheet -> creating one if exception is thrown
    try:
        minecraft_sheet = gc.open(name)
        print('Opened spreadsheet', name)

        try:
            # updating appropriate worksheet by updating the sheet via csv import
            minecraft_sheet.values_update(
                            name_csv,
                            params={'valueInputOption': 'USER_ENTERED'},
                            body={'values': list(csv.reader(open(csvFile)))}
            )
            print('Update successful!')

        except gspread.exceptions.APIError:

            print('Worksheet not found! - Creating new worksheet with data...')

            # creating new worksheet
            minecraft_sheet.add_worksheet(title=name_csv, rows="200", cols="10")

            # updating appropriate worksheet by updating the sheet via csv import
            minecraft_sheet.values_update(
                            name_csv,
                            params={'valueInputOption': 'USER_ENTERED'},
                            body={'values': list(csv.reader(open(csvFile)))}
            )
            print('Worksheet created and updated successfully!')

    except gspread.exceptions.SpreadsheetNotFound:
        # creating new spreadsheet for new player in minecraft stats proj folder
        print('Spreadsheet did not exist for', name, 'Creating and opening one for them now.')
        drive_service = discovery.build('drive', 'v3', credentials = creds)
        file_metadata = {
                        'name': name,
                        'mimeType': 'application/vnd.google-apps.spreadsheet',
                        'parents': [dest_folder_id]
                        }
        file = drive_service.files().create(body=file_metadata).execute()
        minecraft_sheet = gc.open(name)
        print('Created and opened spreadsheet!')

        print('Creating new worksheet and updating with data...')
        # creating new worksheet
        minecraft_sheet.add_worksheet(title=name_csv, rows="200", cols="10")

        # updating appropriate worksheet by updating the sheet via csv import
        minecraft_sheet.values_update(
                        name_csv,
                        params={'valueInputOption': 'USER_ENTERED'},
                        body={'values': list(csv.reader(open(csvFile)))}
        )
        print('Worksheet created and updated successfully!')

    print('-------------------------------------------------------------------')
    # sleeping 3 seconds to avoid quota limit
    time.sleep(3)

################################################################################
# initializing the program
if __name__ == '__main__':
    dir_to_usercache = '/Users/lmiller/PythonProjects/MinecraftStats/jsons/usercache.json'
    dir_to_jsons = '/Users/lmiller/PythonProjects/MinecraftStats/jsons/stats/'
    CreateCSV(dir_to_usercache, dir_to_jsons)
