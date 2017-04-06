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

Boxscores_DATA = 'boxscores/ncaaf_players.csv'
Players_DATA = 'positions/ncaaf_positions.csv'

csvfile = open('tie_occurence/ncaaf_tie_occurence.csv', 'w')
fieldnames = ['Date','Position','Points','Count','Position_Count']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    games = pandas.read_csv(Boxscores_DATA)
    players = pandas.read_csv(Players_DATA)

    round_map = lambda points: round(points, 1)

    games = games[['Year','Date','GameID','PlayerName','Fantasy_Points']]

    games = merge(games, players, on=['Year','PlayerName'], how='left')

    games_fields = ['Date',
                    'GameID',
                    'PlayerName',
                    'Position',
                    'Fantasy_Points']
    games = games[games_fields]
    games.Fantasy_Points = games.Fantasy_Points.map(round_map)
    games = games[games.Fantasy_Points > 0].sort('Fantasy_Points')

    quarterbacks = games[games.Position == 'QB'].sort('Fantasy_Points')
    runningbacks = games[games.Position == 'RB'].sort('Fantasy_Points')
    widereceivers = games[games.Position =='WR'].sort('Fantasy_Points')
    tightends = games[games.Position == 'TE'].sort('Fantasy_Points')

    dates = games['Date'].unique()
    dates.sort()
    for i in range(0,len(dates)):
        #Contest will only be run on Single Days when there are 5 or more games available.
        date = dates[i]
        gameids = games[games.Date == date]['GameID'].unique()

        try:
            date_quarterbacks = quarterbacks[quarterbacks.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_runningbacks = runningbacks[runningbacks.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_widereceivers = widereceivers[widereceivers.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_tightends = tightends[tightends.Date == date].sort('Fantasy_Points', ascending=False).reset_index()

            for position in (date_quarterbacks, date_runningbacks, date_widereceivers, date_tightends):
                no_tie = True
                pos = position.Position[0]
                pos_count = len(position)
                point_ranges = position.Fantasy_Points.unique()

                for points in point_ranges:
                    count = len(position[position.Fantasy_Points == points])
                    points = round(points, 1)
                
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
