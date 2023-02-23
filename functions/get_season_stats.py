from pyAFL.seasons.models import Season

import pandas as pd

def get_season_stats(start_year, end_year):
    '''
    Function to collect multiple seasons of data in one request
    '''

    games = pd.DataFrame()
    
    for year in range(start_year, end_year+1):
        season = Season(year)
        stats = season.get_season_stats()
        stats_match = stats.match_summary
        games = pd.concat([games, stats_match], axis=0)

    games.reset_index(inplace=True, drop=True)
    games = games.rename(columns={'Home team':'Home Team'})

    return games