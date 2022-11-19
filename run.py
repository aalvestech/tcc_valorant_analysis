from crawler import Crawler
from data_cleaner import DataCleaner


server_list = ['br', 'latam', 'na', 'eu', 'kr', 'ap']

df_top500 = Crawler.get_top500(server_list)
df_top500_abt = DataCleaner.clean_top500(df_top500)
df_top500_abt.head(5)

df_matches_report = Crawler.get_matches_report(df_top500_abt['nickNameFull'])
df_matches = DataCleaner.clean_matches(df_matches_report, df_top500_abt)
df_matches.head(5)

weapons_report = Crawler.get_top500_players_weapons_report(df_top500_abt['nickNameFull'])
df_weapons = DataCleaner.clean_weapons(weapons_report)
weapons_report.head(5)




