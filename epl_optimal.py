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
import Universal_Optimizer as uo
from collections import defaultdict

Boxscores_DATA = 'boxscores/epl_players.csv'

POSITIONS = ['F1','F2','M1','M2','D1','D2','U1','U2','G']

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
                 'SW': 'S'}

Position_DICT = defaultdict(lambda: 'S', Position_DICT)

csvfile = open('optimals/epl_optimal_lineups.csv', 'w')
fieldnames = ['Date','Player_ID_F1','Player_ID_F2','Player_ID_M1','Player_ID_M2','Player_ID_D1','Player_ID_D2','Player_ID_U1','Player_ID_U2','Player_ID_G','Dollars','Points']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    CURR_DATE = datetime.datetime.now() + datetime.timedelta(hours=-4) + datetime.timedelta(minutes=5)
    time = CURR_DATE.strftime('%H:%M')

    games = pandas.read_csv(Boxscores_DATA)

    position_map = lambda position: Position_DICT[position]

    games['Position'] = games['Position'].map(position_map)
    games['Points'] = games['Fantasy_Points']
    games['Dollars'] = games['Salary']

    games_fields = ['PlayerID',
                    'Date',
                    'Position',
                    'Points',
                    'Dollars']
    games = games[games_fields]
    games = games[games.Points > 0].sort('Points')

    dates = games['Date'].unique()
    dates.sort()
    for i in range(0,len(dates)):
        date = dates[i]
        results_df = games[games.Date == date][['PlayerID','Position','Points','Dollars']]

        optimizer = uo.LineupOptimizer(results_df,
                                       POSITIONS,
                                       50000,
                                       40000,
                                       1,
                                       CURR_DATE.year,
                                       CURR_DATE.month,
                                       CURR_DATE.day)

        lineup = optimizer.calc_lineup()
        if len(lineup) > 0:
            lineup['Date'] = date
            data = {'Date': date,
                    'Player_ID_F1': lineup.values[0][0],
                    'Player_ID_F2': lineup.values[0][1],
                    'Player_ID_M1': lineup.values[0][4],
                    'Player_ID_M2': lineup.values[0][5],
                    'Player_ID_D1': lineup.values[0][6],
                    'Player_ID_D2': lineup.values[0][7],
                    'Player_ID_U1': lineup.values[0][8],
                    'Player_ID_U2': lineup.values[0][9],
                    'Player_ID_G': lineup.values[0][10],
                    'Dollars': lineup.values[0][2],
                    'Points': lineup.values[0][3]}
            writer.writerow(data)


if __name__ == "__main__":
    main()
