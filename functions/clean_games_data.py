import pandas as pd

def clean_games_data(games_df, team_code_df, table_hist_df):
    '''
    Function to clean the games data and join with the table dataframe
    '''
    
    # Fix team names
    team_name_fixes = {'Footscray': 'Western Bulldogs', 'Kangaroos': 'North Melbourne', 'South Melbourne':'Sydney'}
    games_df = games_df.replace(team_name_fixes)

    # Fix the round for finals games to join to the table
    games_df['Round'] = games_df['Round'].apply(lambda x: 24 if x > 24 else x)

    # Tag the early part of the season to account for variability from season to season
    games_df['Year stage'] = games_df.apply(lambda x: 'Finals' if 'Final' in x['Year stage'] else('Early season' if x['Round'] < 4 else x['Year stage']), axis=1)

    # Split the Date time for match stats fetch
    games_df[['day', 'month', 'year']] = games_df['Date'].dt.strftime('%d-%m-%Y').str.split('-', expand=True)
    games_df['time'] = games_df['Date'].dt.time
    games_df['year'] = games_df['year'].astype(int)

    # Add a leading zero to month & day
    games_df['month'] = games_df['month'].apply(lambda x: x.zfill(2))
    games_df['day'] = games_df['day'].apply(lambda x: x.zfill(2))

    # Add two columns to enable a join of the first round to the last round
    games_df['round_key'] = games_df['Round'].apply(lambda x: 24 if x == 1 else x)
    games_df['year_key'] = games_df.apply(lambda x: x['year'] - 1 if x['Round'] == 1 else x['year'], axis=1)
    
    # Merge all the tables together in preparation for the detailed stats
    games_df = pd.merge(games_df, team_code_df[['Team','Code']], left_on='Home team', right_on='Team', how='left')
    games_df = games_df.drop('Team', axis=1)
    games_df = games_df.rename(columns={'Code':'HomeCode'})

    games_df = pd.merge(games_df, team_code_df[['Team','Code']], left_on='Away Team', right_on='Team', how='left')
    games_df = games_df.drop('Team', axis=1)
    games_df = games_df.rename(columns={'Code':'AwayCode'})

    games_df = pd.merge(games_df, table_hist_df, left_on=['Home team','round_key','year_key'], right_on=['Team','Round','Year'], how='left')
    games_df = pd.merge(games_df, table_hist_df, left_on=['Away Team','round_key','year_key'], right_on=['Team','Round','Year'], suffixes=('_home','_away'), how='left')

    games_df = games_df.dropna(subset=['Team_home'])
    games_df.reset_index(inplace=True)
    
    return games_df