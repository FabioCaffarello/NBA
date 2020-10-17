#Method to extract the information of players per season
def scrape_season_stats(base_url, year_start, year_end):
    '''
    Function to Extract NBA seasons Data
    '''
    
    #Libraries
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup

    #Create Range of Years Scraping
    years = range(year_start,year_end+1,1)

    #Start DataFrame
    df_season = pd.DataFrame()

    #Do task for all years in range
    for year in years:

        try:
            #Message
            print(f'Extracting data from the {year} season')

            #Request
            request_url = base_url.format(year)
            req = requests.get(request_url)

            #Get Html Content
            soup = BeautifulSoup(req.content, 'html.parser')
            table = soup.find('table', {'id':'totals_stats'})

            #Convert in Pandas DataFrame
            df = pd.read_html(str(table))[0]

            #Save Control Info
            df['Year'] = year
            df['Season'] = f'{year-1}-{str(year)[2:]}'

            #Append Year
            df_season = df_season.append(df)
        
        except Exception as excp:
            #Message
            print(f'Problem Extracting data from the {year} season')
            print(excp)
            
    #Filter RK
    df_season_clean = df_season[~(df_season['Rk'] == 'Rk')]

    #Return Data    
    return df_season_clean

#Method to extract the information of all seasons
def scrape_all_seasons(base_url):
    '''
    Function to Extract All NBA seasons Data
    '''
    
    #Libraries
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup

    try:
        #Request
        req = requests.get(base_url)
        
        #Scrape
        soup = BeautifulSoup(req.content, 'html.parser')
        table = soup.find('table', {'id':'stats'})

        #Return df
        df_total = pd.read_html(str(table))[0]
        df_total.columns = df_total.columns.droplevel()
    
    except Exception as excp:
        #Message
        print(f'Problem Extracting All Season')
        print(excp)

    return(df_total)