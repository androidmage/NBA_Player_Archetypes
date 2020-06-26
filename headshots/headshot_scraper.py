#%% get all players to scrape
import pandas as pd
import urllib.request

player_ids = []

for year in range(2014, 2020):
    yearDf = pd.read_csv('data/playerTotals' + str(year) + '.csv', sep=',')
    player_ids += yearDf['slug'].tolist()

# remove duplicates and sort list
player_ids = sorted(list(set(player_ids)), key=str.lower)

#%% scrape all players for headshot
url = 'https://d2cwpp38twqe55.cloudfront.net/req/202006161/images/players/'

for player_id in player_ids:
    urllib.request.urlretrieve(url + player_id + '.jpg',
                               'headshots/scraper_output/' + player_id + '.jpg')