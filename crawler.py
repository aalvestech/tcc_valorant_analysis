import pandas as pd
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from datetime import date, datetime

class Crawler():

    def get_top500(servers_list) -> str:
        '''
            This function's mission is to get all players that are ranked in the top 500 of a server list.
            :param [list] server_list: A variable that receives a server list. For example: 'kr', 'eu', 'na', 'br', 'latam', 'ap'.
            :return [pd.dataframe] data: A variable that receives a string with the structure of a json. This string contains the summarized information of a player that who's in top 500.
        '''
        print('##########################################################################')
        print('Iniciando o Crawler dos top500 dos servidores {}'.format(servers_list))
        print('##########################################################################')

        file_name = 'top500_all_servers_{}.csv'.format(datetime.today().strftime('%Y%m%d%H%M'))
        data = []
        df = pd.DataFrame()
        total_servers = len(servers_list)

        print('\nIremos processar um total de {} server: '.format(total_servers))

        for server in servers_list:

            print('\nProcessando o servers {}'.format(server))
            
            for page in range(1, 5):

                response = requests.get('https://val.dakgg.io/api/v1/leaderboards/{}/aca29595-40e4-01f5-3f35-b1b3d304c96e?page={}&tier=top500'.format(server, page))
                data_aux = response.json()
                data.append(data_aux)

        df = pd.DataFrame(data)
        df = pd.json_normalize(json.loads(df.to_json(orient='records'))).explode('leaderboards')
        df = pd.json_normalize(json.loads(df.to_json(orient='records')))

        df['leaderboards.full_nickname'] = (df['leaderboards.gameName'].map(str) + '%23' + df['leaderboards.tagLine'].map(str))

        print('\nSalvando o arquivo top500_all_servers.csv na pasta data')
        df.to_csv('C:\\repos\\tcc_valorant_analysis\\data\\top_500\\{}'.format(file_name))
        print('\nArquivo salvo!')
 
        return df

    def get_matches_report(players_list) -> str:
        '''
            This function's mission is to get a summary report of all the last 200 matches of a specific player.
            :param [list] players_list: A variable that receives a players list. For example: ['NaraKa%232299','NakaRa%233265','RayzenSama%236999'].
            :return [str] data_pre: A variable that receives a string with the structure of a json. This string contains the summarized information of a player who's in the top 500.
        '''

        print('##########################################################################')
        print('Iniciando o Crawler dos das partidas')
        print('##########################################################################')

        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', options = options)

        driver = webdriver.Chrome(ChromeDriverManager().install())  

        data = []
        count_players = 0
        total_players = len(players_list)
        file_name = 'matches_summarized_{}.csv'.format(datetime.today().strftime('%Y%m%d%H%M'))

        print('\nIremos processar um total de {} players: '.format(total_players))


        for player in players_list:

            count_players += 1 
            
            print('\nProcessando os dados do player {} ({} de {})'.format(player, count_players, total_players))

            for page in range(1,10):

                driver.get('https://api.tracker.gg/api/v2/valorant/standard/matches/riot/{}?type=competitive&next={}'.format(player, page))
                time.sleep(2)
                data_pre = driver.find_element('xpath', '//pre').text
                data_json = json.loads(data_pre)

                if 'data' in data_json.keys():
                    matches = data_json['data']['matches']

                    for match in matches:

                        dataframe_row = dict()
                        dataframe_row['player'] = player
                        dataframe_row['matchId'] = match['attributes']['id']
                        dataframe_row['mapId'] = match['attributes']['mapId']
                        dataframe_row['modeId'] = match['attributes']['modeId']
                        dataframe_row['modeKey'] = match['metadata']['modeKey']
                        dataframe_row['modeName'] = match['metadata']['modeName']
                        dataframe_row['modeImageUrl'] = match['metadata']['modeImageUrl']
                        dataframe_row['modeMaxRounds'] = match['metadata']['modeMaxRounds']
                        dataframe_row['isAvailable'] = match['metadata']['isAvailable']
                        dataframe_row['timestamp'] = match['metadata']['timestamp']
                        dataframe_row['metadataResult'] = match['metadata']['result']
                        dataframe_row['map'] = match['metadata']['map']
                        dataframe_row['mapName'] = match['metadata']['mapName']
                        dataframe_row['mapImageUrl'] = match['metadata']['mapImageUrl']
                        dataframe_row['seasonName'] = match['metadata']['seasonName']
                        dataframe_row['userId'] = match['segments'][0]['attributes']['platformUserIdentifier']
                        dataframe_row['hasWon'] = match['segments'][0]['metadata']['hasWon']
                        dataframe_row['result'] = match['segments'][0]['metadata']['result']
                        dataframe_row['agentName'] = match['segments'][0]['metadata']['agentName']

                        for stat_name, stat_value in match['segments'][0]['stats'].items():

                            dataframe_row[f"{stat_name}Value"] = stat_value['value']
                            dataframe_row[f"{stat_name}DisplayValue"] = stat_value['displayValue']
                            dataframe_row[f"{stat_name}DisplayType"] = stat_value['displayType']

                        data.append(dataframe_row)
                

        df = pd.DataFrame.from_dict(data)

        print('Salvando o arquivo matches_summarized.csv na pasta data')
        df.to_csv('C:\\repos\\tcc_valorant_analysis\\data\\matches\\{}'.format(file_name),index=False)
        print('Arquivo salvo')
        
        driver.quit()

        return df

    def get_top500_players_weapons_report(players_list) -> str:
        '''
            This function's mission is to get a summary report of all the last 200 matches of a specific player.
            :param [list] players_list: A variable that receives a players list. For example: ['NaraKa%232299','NakaRa%233265','RayzenSama%236999'].
            :return [str] data_pre: A variable that receives a string with the structure of a json. This string contains the summarized information of a player who's in the top 500.
        '''

        print('##########################################################################')
        print('Iniciando o Crawler dos das armas')
        print('##########################################################################')

        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', options = options)

        file_name = 'weapons_summarized_{}.csv'.format(datetime.today().strftime('%Y%m%d%H%M'))
        data = []
        driver = webdriver.Chrome(ChromeDriverManager().install())  


        for player in players_list:

            print('Processando os dados do player {}'.format(player))

            driver.get('https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{}/segments/weapon?playlist=competitive&seasonId=default'.format(player))
            data_pre = driver.find_element('xpath', '//pre').text
            data_json = json.loads(data_pre)

            if 'data' in data_json.keys():
                weapons = data_json['data']

                for weapon in weapons:
                    dataframe_row = dict()
                    dataframe_row['player'] = player
                    dataframe_row['weaponName'] = weapon['attributes']['key']

                    for stat_name, stat_value in weapon['stats'].items():
                        dataframe_row[f"{stat_name}Value"] = stat_value['value']
                        dataframe_row[f"{stat_name}DisplayValue"] = stat_value['displayValue']
                        dataframe_row[f"{stat_name}DisplayType"] = stat_value['displayType']

                    data.append(dataframe_row)

        
        df = pd.DataFrame.from_dict(data)
        
        print('Salvando o arquivo weapons_summarized.csv na pasta data')
        df.to_csv('C:\\repos\\tcc_valorant_analysis\\data\\{}'.format(file_name),index=False)
        print('Arquivo salvo!')

        driver.quit()

        return df