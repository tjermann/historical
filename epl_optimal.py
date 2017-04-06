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

csvfile = open('optimals/epl_optimal_lineups.csv', 'w')
fieldnames = ['Date','F1','F2','M1','M2','D1','D2','U1','U2','G','Total']
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
            date_utilities = [date_forwards['Fantasy_Points'][2], date_forwards['Fantasy_Points'][3],  date_defenders['Fantasy_Points'][2], date_defenders['Fantasy_Points'][3], date_midfielders['Fantasy_Points'][2], date_midfielders['Fantasy_Points'][3]]
            date_utilities.sort(reverse=True)
        

            f1_points = round(date_forwards['Fantasy_Points'][0],1)
            f2_points = round(date_forwards['Fantasy_Points'][1],1)
            m1_points = round(date_midfielders['Fantasy_Points'][0],1)
            m2_points = round(date_midfielders['Fantasy_Points'][1],1)
            d1_points = round(date_defenders['Fantasy_Points'][0],1)
            d2_points = round(date_defenders['Fantasy_Points'][1],1)
            u1_points = round(date_utilities[0],1)
            u2_points = round(date_utilities[1],1)
            g_points = round(date_goalies['Fantasy_Points'][0],1)
 
            lineup_points = round(f1_points + f2_points+ m1_points + m2_points + d1_points + d2_points + u1_points + u2_points + g_points,1)

            data = {'Date': date,
                    'F1': f1_points,
                    'F2': f2_points,
                    'M1': m1_points,
                    'M2': m2_points,
                    'D1': d1_points,
                    'D2': d2_points,
                    'U1': u1_points,
                    'U2': u2_points,
                    'G': g_points,
                    'Total': lineup_points}

            if len(gameids) >= 5:
                writer.writerow(data)

        except Exception:
            continue


if __name__ == "__main__":
    main()
