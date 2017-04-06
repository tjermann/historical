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

csvfile = open('tie_occurence/mlb_tie_occurence.csv', 'w')
fieldnames = ['Date','Position','Points','Count','Position_Count']
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
    outfielders.Position = 'OF'
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

            for position in (date_catchers, date_firstbasemen, date_secondbasemen, date_shortstops, date_thirdbasemen, date_outfielders, date_pitchers):

                no_tie = True
                pos = position.Position[0]
                pos_count = len(position)
                point_ranges = position.Fantasy_Points.unique()

                for points in point_ranges:
                    count = len(position[position.Fantasy_Points == points])
                
                    if count>1:
                        no_tie = False
 
                        data = {'Date': date,
                                'Position': pos,
                                'Points': points,
                                'Count': count,
                                'Position_Count': pos_count}

                        writer.writerow(data)

                if no_tie == True:
                    data = {'Date': date,
                            'Position': pos,
                            'Points': 'NT',
                            'Count': 'NT',
                            'Position_Count': pos_count}
                    writer.writerow(data)

        except Exception:
            pass
                           



if __name__ == "__main__":
    main()
