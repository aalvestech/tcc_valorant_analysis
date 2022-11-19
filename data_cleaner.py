import pandas as pd

class DataCleaner():

    def clean_top500(df) -> pd.DataFrame:

        # df_top500_all_servers_raw = pd.read_csv('C:\\repos\\tcc_valorant_analysis\\data\\top_500\\top500_all_servers_17_11_2022_20_26.csv')

        df_top500 = df[['meta.shard', 'meta.updatedAt', 'leaderboards.gameName','leaderboards.tagLine',
                                                  'leaderboards.full_nickname','leaderboards.leaderboardRank','leaderboards.rankedRating',
                                                  'leaderboards.numberOfWins', 'leaderboards.competitiveTier','leaderboards.stat.winRatio',
                                                  'leaderboards.stat.avgScore', 'leaderboards.stat.headshotRatio',]]

        df_top500_renamed = df_top500.rename(columns={'meta.shard': 'server', 'meta.updatedAt': 'updatedAt',
                                      'leaderboards.gameName': 'gameName', 'leaderboards.tagLine': 'tagLine',
                                      'leaderboards.full_nickname': 'nickNameFull', 'leaderboards.leaderboardRank': 'leaderboardRank',
                                      'leaderboards.rankedRating': 'rankedRating', 'leaderboards.numberOfWins': 'numberOfWins',
                                      'leaderboards.competitiveTier': 'competitiveTier', 'leaderboards.stat.winRatio': 'winRatio',
                                      'leaderboards.stat.avgScore': 'avgScore', 'leaderboards.stat.headshotRatio': 'headshotRatio',})

        df_top500_abt = df_top500_renamed.dropna().reset_index(drop=True)

        df_top500_abt.to_csv('C:\\repos\\tcc_valorant_analysis\\data\\top_500\\top500_abt.csv')

        return df_top500_abt

    
    def clean_matches(df, df_top500_abt) -> pd.DataFrame:

        df_matches = df[[
                                        'player', 'matchId', 'mapId', 'modeId', 'modeKey',
                                        'modeName', 'modeImageUrl', 'modeMaxRounds', 'isAvailable',
                                        'timestamp', 'metadataResult', 'map', 'mapName', 'mapImageUrl',
                                        'seasonName', 'userId', 'hasWon', 'result', 'agentName', 'playtimeValue',
                                        'playtimeDisplayValue', 'playtimeDisplayType', 'roundsPlayedValue',
                                        'roundsPlayedDisplayValue', 'roundsPlayedDisplayType', 'roundsWonValue',
                                        'roundsWonDisplayValue', 'roundsWonDisplayType', 'roundsLostValue',
                                        'roundsLostDisplayValue', 'roundsLostDisplayType', 'roundsDisconnectedValue',
                                        'roundsDisconnectedDisplayValue', 'roundsDisconnectedDisplayType', 'placementValue',
                                        'placementDisplayValue', 'placementDisplayType', 'scoreValue', 'scoreDisplayValue',
                                        'scoreDisplayType', 'killsValue', 'killsDisplayValue', 'killsDisplayType', 'deathsValue',
                                        'deathsDisplayValue', 'deathsDisplayType', 'assistsValue', 'assistsDisplayValue',
                                        'assistsDisplayType', 'damageValue', 'damageDisplayValue', 'damageDisplayType',
                                        'damageReceivedValue', 'damageReceivedDisplayValue', 'damageReceivedDisplayType',
                                        'headshotsValue', 'headshotsDisplayValue', 'headshotsDisplayType', 'grenadeCastsValue',
                                        'grenadeCastsDisplayValue', 'grenadeCastsDisplayType', 'ability1CastsValue',
                                        'ability1CastsDisplayValue', 'ability1CastsDisplayType', 'ability2CastsValue',
                                        'ability2CastsDisplayValue', 'ability2CastsDisplayType', 'ultimateCastsValue',
                                        'ultimateCastsDisplayValue', 'ultimateCastsDisplayType', 'dealtHeadshotsValue',
                                        'dealtHeadshotsDisplayValue', 'dealtHeadshotsDisplayType', 'dealtBodyshotsValue',
                                        'dealtBodyshotsDisplayValue', 'dealtBodyshotsDisplayType', 'dealtLegshotsValue',
                                        'dealtLegshotsDisplayValue', 'dealtLegshotsDisplayType', 'econRatingValue',
                                        'econRatingDisplayValue', 'econRatingDisplayType', 'suicidesValue', 'suicidesDisplayValue',
                                        'suicidesDisplayType', 'revivedValue', 'revivedDisplayValue', 'revivedDisplayType',
                                        'firstBloodsValue', 'firstBloodsDisplayValue', 'firstBloodsDisplayType', 'firstDeathsValue',
                                        'firstDeathsDisplayValue', 'firstDeathsDisplayType', 'lastDeathsValue', 'lastDeathsDisplayValue',
                                        'lastDeathsDisplayType', 'survivedValue', 'survivedDisplayValue', 'survivedDisplayType', 'tradedValue',
                                        'tradedDisplayValue', 'tradedDisplayType', 'kastedValue', 'kastedDisplayValue', 'kastedDisplayType',
                                        'kASTValue', 'kASTDisplayValue', 'kASTDisplayType', 'flawlessValue', 'flawlessDisplayValue',
                                        'flawlessDisplayType', 'thriftyValue', 'thriftyDisplayValue', 'thriftyDisplayType', 'acesValue',
                                        'acesDisplayValue', 'acesDisplayType', 'teamAcesValue', 'teamAcesDisplayValue', 'teamAcesDisplayType',
                                        'clutchesValue', 'clutchesDisplayValue', 'clutchesDisplayType', 'clutchesLostValue', 'clutchesLostDisplayValue',
                                        'clutchesLostDisplayType', 'plantsValue', 'plantsDisplayValue', 'plantsDisplayType', 'defusesValue',
                                        'defusesDisplayValue', 'defusesDisplayType', 'kdRatioValue', 'kdRatioDisplayValue', 'kdRatioDisplayType',
                                        'scorePerRoundValue', 'scorePerRoundDisplayValue', 'scorePerRoundDisplayType', 'damagePerRoundValue',
                                        'damagePerRoundDisplayValue', 'damagePerRoundDisplayType', 'headshotsPercentageValue', 'headshotsPercentageDisplayValue',
                                    ]]

        df_matches = df_matches.rename(columns={'player': 'nickNameFull'})

        df_matches_abt = df_matches.merge(df_top500_abt[["nickNameFull", "leaderboardRank", 'competitiveTier', 'rankedRating']])

        df_matches_abt.to_csv('C:\\repos\\tcc_valorant_analysis\\data\\matches\\matches_abt.csv')

        return df_matches_abt

    
    def clean_weapons(df) -> pd.DataFrame:

        # df_weapons_raw = pd.read_csv('C:\\repos\\tcc_valorant_analysis\\data\\weapons\\weapons_summarized_20221172029.csv', low_memory=False)

        df_weapons = df[[
                                        'player','weaponName','matchesPlayedValue', 'matchesWonValue',
                                        'matchesLostValue', 'matchesTiedValue','matchesWinPctValue','roundsPlayedValue',
                                        'killsValue','killsPerRoundValue','killsPerMatchDisplayValue',
                                        'secondaryKillsValue','headshotsValue','secondaryKillsPerRoundDisplayValue',
                                        'secondaryKillsPerMatchDisplayValue','deathsValue','deathsPerRoundDisplayValue',
                                        'deathsPerMatchDisplayValue','kDRatioValue','kDRatioDisplayValue','headshotsPercentageValue',
                                        'damageValue','damagePerRoundValue','damagePerMatchValue','damageReceivedValue',
                                        'dealtHeadshotsValue','dealtBodyshotsValue','dealtLegshotsValue','killDistanceValue',
                                        'killDistanceDisplayValue','avgKillDistanceValue','avgKillDistanceDisplayValue',
                                        'longestKillDistanceValue','longestKillDistanceDisplayValue',
                                    ]]

        df_weapons_abt = df_weapons.rename(columns={'player': 'nickNameFull'})

        df_weapons_abt.to_csv('C:\\repos\\tcc_valorant_analysis\\data\\weapons\\weapons_summarized_abt.csv')

        return df_weapons_abt

