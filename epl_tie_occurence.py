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

Boxscores_DATA = 'boxscores/epl_players.csv'

Position_DICT = {'G': 'G',
                 'CD-R': 'D',
                 'CD' :'D',
                 'CD-L': 'D',
                 'AM' : 'M',
                 'LM': 'M',
                 'RM': 'M',
                 'CF-L' : 'F',
                 'CF-R': 'F',
                 'RB': 'D',
                 'LB': 'D',
                 'M' : 'M',
                 'CM': 'M',
                 'CM-L': 'M',
                 'CM-R': 'M',
                 'D': 'D',
                 'F': 'F',
                 'AM-L': 'M',
                 'AM-R': 'M',
                 'RCF': 'F',
                 'DM': 'M',
                 'LF': 'F',
                 'RF': 'F',
                 'Sub': 'S',
                 'S': 'S',
                 'SW': 'D'}

csvfile = open('tie_occurence/epl_tie_occurence.csv', 'w')
fieldnames = ['Date','Position','Points','Count','Position_Count']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    games = pandas.read_csv(Boxscores_DATA)

    position_map = lambda position: Position_DICT[position]

    games['Position'] = games['Position'].map(position_map)

    games_fields = ['Date',
                    'GameID',
                    'PlayerName',
                    'Position',
                    'Fantasy_Points']
    games = games[games_fields]
    games = games[games.Fantasy_Points > 0].sort('Fantasy_Points')

    forwards = games[games.Position == 'F'].sort('Fantasy_Points')
    midfielders = games[games.Position == 'M'].sort('Fantasy_Points')
    defenders = games[games.Position == 'D'].sort('Fantasy_Points')
    goalies = games[games.Position == 'G'].sort('Fantasy_Points')

    dates = games['Date'].unique()
    dates.sort()
    for i in range(0,len(dates)):
        #Contest will only be run on Single Days when there are 5 or more games available.
        date = dates[i]
        gameids = games[games.Date == date]['GameID'].unique()

        try:

            date_forwards = forwards[forwards.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_defenders = defenders[defenders.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_midfielders = midfielders[midfielders.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_goalies = goalies[goalies.Date == date].sort('Fantasy_Points', ascending=False).reset_index()

            date_goalies = goalies[goalies.Date == date].sort('Fantasy_Points', ascending=False).reset_index()

            for position in (date_forwards, date_defenders, date_midfielders, date_goalies):
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
