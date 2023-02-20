def clean_table_data(df):
    '''
    Function to clean the table dataframe
    '''

    # Pre process table data
    df['Round'] = df['Round'].astype(int)
    df['Team'] = df['Team'].replace('GWS Giants','Greater Western Sydney')
    
    # Drop 12 month ago columns
    df = df.drop(['Pos12', 'W12', 'D12', 'L12', 'Pts12', '12%'], axis=1)

    # Strip out the for and against value
    df['For'] = df['For'].str.replace(r" \(.*\)", "")
    df['Agn'] = df['Agn'].str.replace(r" \(.*\)", "")

    # Fix the Streak column
    df[['Stkn', 'Stkd']] = df['Stk'].str.split('(\d+)([A-Za-z]+)', expand=True).loc[:, [1, 2]]
    
    # drop NA rows
    df = df.dropna()

    # Convert the Stkn to an int and then mulitple a loss by negative to create a minus value
    df['Stkn'] = df['Stkn'].astype(int)
    df.loc[df['Stkd'] == 'L', 'Stkn'] *= -1
    df.loc[df['Stkd'] == 'D', 'Stkn'] = 0
    return df