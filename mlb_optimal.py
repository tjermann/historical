from pandas import * 
import pandasql
import numpy as np
import MySQLdb as mdb
import sys
import string
import pdb
import datetime
from random import randint
import csv

Boxscores_DATA = 'boxscores/mlb_hitters.csv'
Pitchers_DATA = 'boxscores/mlb_pitchers.csv'

csvfile = open('optimals/mlb_optimal_lineups.csv', 'w')
fieldnames = ['Date','P','C','1B','2B','SS','3B','OF1','OF2','OF3','Total']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    games = pandas.read_csv(Boxscores_DATA)
    pitchers = pandas.read_csv(Pitchers_DATA)

    pitchers['Position'] = 'P'

    games_fields = ['Date',
                    'GameID',
                    'PlayerName',
                    'Position',
                    'Fantasy_Points']
    games = games[games_fields]
    games = games[games.Fantasy_Points > 0].sort('Fantasy_Points')
    pitchers = pitchers[games_fields]
    pitchers = pitchers[pitchers.Fantasy_Points > 0].sort('Fantasy_Points')

    catchers = games[games.Position == 'C'].sort('Fantasy_Points')
    firstbasemen = games[games.Position == '1B'].sort('Fantasy_Points')
    secondbasemen = games[games.Position == '2B'].sort('Fantasy_Points')
    shortstops = games[games.Position == 'SS'].sort('Fantasy_Points')
    thirdbasemen = games[games.Position == '3B'].sort('Fantasy_Points')
    outfielders = games[games.Position.isin(['OF','DH','PH'])].sort('Fantasy_Points')
    pitchers = pitchers.sort('Fantasy_Points')

    dates = games['Date'].unique()
    dates.sort()
    for i in range(0,len(dates)):
        #Contest will only be run on Single Days when there are 5 or more games available.
        date = dates[i]
        gameids = games[games.Date == date]['GameID'].unique()

        try:

            date_catchers = catchers[catchers.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_firstbasemen = firstbasemen[firstbasemen.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_secondbasemen = secondbasemen[secondbasemen.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_shortstops = shortstops[shortstops.Date == date].sort('Fantasy_Points', ascending = False).reset_index()
            date_thirdbasemen = thirdbasemen[thirdbasemen.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_outfielders = outfielders[outfielders.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_pitchers = pitchers[pitchers.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
        

            p_points = round(date_pitchers['Fantasy_Points'][0],1)
            c_points = round(date_catchers['Fantasy_Points'][0],1)
            b1_points = round(date_firstbasemen['Fantasy_Points'][0],1)
            b2_points = round(date_secondbasemen['Fantasy_Points'][0],1)
            ss_points = round(date_shortstops['Fantasy_Points'][0],1)
            b3_points = round(date_thirdbasemen['Fantasy_Points'][0],1)
            of1_points = round(date_outfielders['Fantasy_Points'][0],1)
            of2_points = round(date_outfielders['Fantasy_Points'][1],1)
            of3_points = round(date_outfielders['Fantasy_Points'][2],1)
 
            lineup_points = round(p_points + c_points+ b1_points + b2_points + ss_points + b3_points + of1_points + of2_points +of3_points,1)

            data = {'Date': date,
                    'P': p_points,
                    'C': c_points,
                    '1B': b1_points,
                    '2B': b2_points,
                    'SS': ss_points,
                    '3B': b3_points,
                    'OF1': of1_points,
                    'OF2': of2_points,
                    'OF3': of3_points,
                    'Total': lineup_points}

            if len(gameids) >= 5:
                writer.writerow(data)

        except Exception:
            continue


if __name__ == "__main__":
    main()
