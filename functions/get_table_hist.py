import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests

def get_table_hist(start_year, end_year, end=23):
    '''

    Parameters
    ----------
    start_year : Date
        The starting year that you wish to extract data for.
    end_year : Date
        The end year that you wish to extract data for.
    end : Integer, optional
        The maximum round that you wish to extract to if you wish it to be shorter than a full season. The default is 23.

    Returns
    -------
    A dataframe history of the AFL ladder at the end of each round.

    '''

    rd = 1
    end = end

    df1 = pd.DataFrame()

    for year in range(start_year, end_year+1):

        while rd <= end:

            url = requests.get(
                f'https://finalsiren.com/AFLLadder.asp?AFLLadderTypeID=2&SeasonID={year}&Round={rd}-1')
            dfs = pd.read_html(url.text)
            data = pd.DataFrame(data=dfs[0])

            if rd == 1:
                data.columns = ['Pos', 'Team', 'P', 'W', 'D', 'L', 'For', 'Agn', 'Max', 'Min', 'Home_W', 'Home_D', 'Home_L', 'Away_W',
                                'Away_D', 'Away_L', 'Stk', 'Pts', '%', 'Pos12', 'W12', 'D12', 'L12', 'Pts12', '12%']
                #data['Chg'] = 'N'
            else:
                data.columns = ['Pos', 'Team', 'P', 'W', 'D', 'L', 'For', 'Agn', 'Max', 'Min', 'Home_W', 'Home_D', 'Home_L', 'Away_W',
                                'Away_D', 'Away_L', 'Stk', 'Chg', 'Pts', '%', 'Pos12', 'W12', 'D12', 'L12', 'Pts12', '12%']
                data = data.drop('Chg', axis=1)

            rstring = str(rd+1)
            data['Round'] = rstring
            data['Year'] = year

            df1 = pd.concat((df1,data), axis=0)
            print(f'Round {rd} Season {year} is completed')

            rd += 1
        
        rd = 1

    return df1 