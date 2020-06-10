# %%scraper player information from 13-14 season to 18-19 season

# Import relevant libraries
from requests import get
from bs4 import BeautifulSoup
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import pandas as pd

# player season totals has 21 features and advanced has 27 features
failed_scrapes = []
# Get season stats for all players
for year in range(2015, 2019):
    print(year)
    # client.players_season_totals(season_end_year=year,
    #                              output_type=OutputType.CSV,
    #                              output_file_path="data/seasonTotals" + str(year) + ".csv")
    # client.players_advanced_season_totals(season_end_year=year,
    #                              output_type=OutputType.CSV,
    #                              output_file_path="data/advancedTotals" + str(year) + ".csv")


    # combine season and advanced stats
    season = pd.read_csv('data/seasonTotals' + str(year) + '.csv', sep=',', index_col =0)
    advanced = pd.read_csv('data/advancedTotals' + str(year) + '.csv', sep=',', index_col =0)
    advanced = advanced[advanced.columns.difference(season.columns)]
    totals = pd.concat([season, advanced], axis=1, sort=False)

    # remove players with less than 1000 minutes
    totals = totals[totals.minutes_played > 500]
    
    # remove duplicate players by keeping most minutes played
    max_minutes = totals.groupby('slug').minutes_played.transform(max)
    totals = totals[totals.minutes_played == max_minutes]
    
    # custom scraping
    url = 'https://www.basketball-reference.com/players/'
    per_game_columns = ['FG', 'FGA', '3P', '3PA', '2P', '2PA',
                              'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST',
                              'STL', 'BLK', 'TOV', 'PF', 'PTS']
    shooting_columns = ['FG', 'FGA', 'FG%', "Ast'd", "%Ast'd"]
    shooting_ranges = ['At Rim', '3 to <10 ft', '10 to <16 ft',
                            '16 ft to <3-pt', '3-pt']
    shooting_indices = [2,3,4,9,10]
    physical_stats = pd.DataFrame()
    per_game_stats = pd.DataFrame()
    shotCharts = pd.DataFrame()
    for slug in totals.index:
        print(slug)
        last_initial = slug[0]
        
        # scrape per game stats
        r = get(url + last_initial + '/' + slug + '.html')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # get per game stats
            table = soup.find('table')
            per_game = pd.read_html(str(table))[0]
            per_game.set_index('Season', inplace=True)
            season = str(year-1) + '-' + str(year)[2:4]
            per_game = per_game.loc[season]
            if type(per_game) is pd.DataFrame:
                for index, row in per_game.iterrows():
                    exp_played = totals.loc[slug, 'games_played']
                    exp_started = totals.loc[slug, 'games_started']
                    act_played = int(row['G'])
                    act_started = int(row['GS'])
                    if exp_played==act_played and exp_started==act_started:
                        per_game = row
                        break

            per_game = pd.DataFrame(per_game[per_game_columns]).transpose()                   
            per_game.index = [slug]
            per_game_stats = pd.concat([per_game_stats, per_game])
            
            # get height and weight
            height = soup.select_one('span[itemprop=height]').text.split('-')
            weight = soup.select_one('span[itemprop=weight]').text.replace('lb', '')
            physical = pd.DataFrame(index=[slug], data={
                'height': int(height[0]) * 12 + int(height[1]),
                'weight': int(weight)})
            physical_stats = pd.concat([physical_stats, physical])
            

        # scrape shot charts
        shotChart = pd.DataFrame()
        r = get(url + last_initial + '/' + slug + '/shooting/' + str(year))
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.findAll('table')
            if len(table) > 0:
                shooting = pd.read_html(str(table[0]))[0]
                
                # get stats from each range
                for row in range(9, 18):
                    sRange = shooting.iloc[row, 1]
                    if sRange in shooting_ranges:
                        shots = shooting.iloc[row, shooting_indices]
                        shots.index = [sRange+' '+name for name in shooting_columns]
                        shots = pd.DataFrame(shots).transpose()
                        shots.index = [slug]
                        shotChart = pd.concat([shotChart, shots], axis=1, sort=False)
                shotCharts = pd.concat([shotCharts, shotChart])
            
            else:
                failed_scrapes.append(slug + ' ' + str(year))
                shotCharts = shotCharts.append(pd.Series(name=slug, dtype='float64'))
            

    # set column names to show per game
    per_game_stats.columns = ['per game ' + name for name in per_game.columns]

    # save csv
    totalData = pd.concat([totals, physical_stats, per_game_stats, shotCharts], axis=1, sort=False)
    totalData.to_csv('data/playerTotals' + str(year) + '.csv')

print(failed_scrapes)
