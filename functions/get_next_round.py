import pandas as pd

import requests
import re
from bs4 import BeautifulSoup

from datetime import datetime

def get_next_round():
    url = requests.get(f'https://finalsiren.com')
    dfs = pd.read_html(url.text)
    data = pd.DataFrame(data=dfs[0])
    dlen = len(data.columns)

    if dlen != 10:
        data = pd.DataFrame(data=dfs[9])
    else:
        data

    data = data.rename(columns={'Gnd':'Venue'})

    def convert_date(date_str):
        dt = datetime.strptime(date_str, "%b %d (%a %I:%M%p)")
        current_year = datetime.now().year
        dt = dt.replace(year=current_year)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
        
    # Apply conversion function to "Date" column
    data['Date'] = data['Date'].apply(convert_date).apply(pd.to_datetime)


    # Scrape the round number
    response = requests.get('https://finalsiren.com').text
    soup = BeautifulSoup(response, "lxml")
    
    if dlen != 10:
        rd = soup.find_all('h2')[1].text
    else:
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
