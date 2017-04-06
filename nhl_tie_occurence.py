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

Boxscores_DATA = 'boxscores/nhl_players.csv'
Goalies_DATA = 'boxscores/nhl_goalies.csv'
Players_DATA = 'positions/nhl_positions.csv'

csvfile = open('tie_occurence/nhl_tie_occurence.csv', 'w')
fieldnames = ['Date','Position','Points','Count','Position_Count']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    games = pandas.read_csv(Boxscores_DATA)
    players = pandas.read_csv(Players_DATA)
    goalies = pandas.read_csv(Goalies_DATA)

    goalies['Position'] = 'G'

    games = games[['Year','Date','GameID','PlayerName','Fantasy_Points']]

    games = merge(games, players, on=['Year','PlayerName'], how='left')

    games_fields = ['Date',
                    'GameID',
                    'PlayerName',
                    'Position',
                    'Fantasy_Points']
    games = games[games_fields]
    games = games[games.Fantasy_Points > 0].sort('Fantasy_Points')
    goalies = goalies[games_fields]
    goalies = goalies[goalies.Fantasy_Points > 0].sort('Fantasy_Points')

    wings = games[games.Position.isin(['RW','LW'])].sort('Fantasy_Points')
    wings.Position = 'P'
    centers = games[games.Position == 'C'].sort('Fantasy_Points')
    defenders = games[games.Position == 'D'].sort('Fantasy_Points')
    goalies = goalies.sort('Fantasy_Points')

    dates = games['Date'].unique()
    dates.sort()
    for i in range(0,len(dates)):
        #Contest will only be run on Single Days when there are 5 or more games available.
        date = dates[i]
        gameids = games[games.Date == date]['GameID'].unique()

        try:
            date_wings = wings[wings.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_defenders = defenders[defenders.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_centers = centers[centers.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_goalies = goalies[goalies.Date == date].sort('Fantasy_Points', ascending=False).reset_index()

            for position in (date_wings, date_defenders, date_centers, date_goalies):
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
