import pandas as pd

import requests
import re
from bs4 import BeautifulSoup

from datetime import datetime

def get_next_round_bk():
    url = requests.get(f'https://finalsiren.com')
    dfs = pd.read_html(url.text)

    def convert_date(date_str):
        dt = datetime.strptime(date_str, "%A %B %d, %I:%M%p")
        current_year = datetime.now().year
        dt = dt.replace(year=current_year)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    data = pd.DataFrame(columns=['Home Team', 'Away Team', 'Venue', 'Date'])

    for i in range(9):
        first_col = dfs[i].iloc[:, 0].name
        home_team = first_col[0]
        away_team = first_col[1]
        game = dfs[i].iloc[0, 0]
        venue, date = game.split(' - ')

        temp_data = pd.DataFrame({
            'Home Team': [home_team],
            'Away Team': [away_team],
            'Venue': [venue],
            'Date': [date],
        })

        # Apply conversion function to "Date" column
        temp_data['Date'] = temp_data['Date'].apply(convert_date).apply(pd.to_datetime)
        
        data = data.append(temp_data, ignore_index=True)

        # Scrape the round number
        response = requests.get('https://finalsiren.com').text
        soup = BeautifulSoup(response, "lxml")
        rd = soup.find_all('h2')[0].text

        match = re.search(r'Round (\d+)', rd)

        if match:
            round = int(match.group(1))
            #print(round)
        else:
            round = 24

        data['Round'] = round

        # Add a new column called "Game Number" that counts up from 1 in each row
        data['Game number'] = data.groupby(['Round']).cumcount()+1

        # Fix the venue names & team names
        venue_name_fixes = {'MCG':'M.C.G.','AO':'Adelaide Oval','MRVL':'Docklands','MS':'Carrara','SSS':'Manuka Oval','SCG':'S.C.G.','G':'Gabba','OS':'Perth Stadium','SS':'Kardinia Park'}
        data = data.replace(venue_name_fixes)

        team_name_fixes = {'GWS Giants':'Greater Western Sydney'}
        data = data.replace(team_name_fixes)

        # Tag the early part of the season to account for variability from season to season
        data['Year stage'] = data.apply(lambda x: 'Finals' if x['Round'] == 24 else('Early season' if x['Round'] < 4 else 'Regular season'), axis=1)


        data = data[['Round','Game number','Home Team','Away Team','Venue','Date','Year stage']]

    return data