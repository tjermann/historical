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

#Number of lineups per active day of EPL games (at least 5 games being played)
num_lineups = 1000

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

Boxscores_DATA = 'boxscores/epl_players.csv'

csvfile = open('lineups/epl_lineups.csv', 'w')
fieldnames = ['Date','F1','F2','M1','M2','D1','D2','U1','U2','G','Total']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    games = pandas.read_csv(Boxscores_DATA)

    exclude = set(string.punctuation)
    name_map = lambda name: ''.join(ch for ch in name if ch not in exclude)
    period_map = lambda name: name.replace('.','')
    position_map = lambda position: Position_DICT[position]

    games['Position'] = games['Position'].map(position_map)

    games_fields = ['Date',
                    'GameID',
                    'PlayerID',
                    'Position',
                    'Fantasy_Points']
    games = games[games_fields]
    games = games[games.Fantasy_Points > 0]

    goalies = games[games.Position == 'G'].sort('Fantasy_Points')
    goalies = goalies[int(0.25*len(goalies)):]
    forwards = games[games.Position == 'F'].sort('Fantasy_Points')
    forwards = forwards[int(0.25*len(forwards)):] 
    midfielders = games[games.Position =='M'].sort('Fantasy_Points')
    midfielders = midfielders[int(0.25*len(midfielders)):]
    defenders = games[games.Position == 'D'].sort('Fantasy_Points')
    defenders = defenders[int(0.25*len(defenders)):]
    

    dates = games['Date'].unique()
    dates.sort()
    for date in dates:
        gameids = games[games.Date == date]['GameID'].unique()
        if len(gameids) >5:
            for j in range(0, num_lineups):

                date_goalies = goalies[goalies.Date == date].reset_index()
                date_forwards = forwards[forwards.Date == date].reset_index()
                date_midfielders = midfielders[midfielders.Date == date].reset_index()
                date_defenders = defenders[defenders.Date == date].reset_index()

                a = randint(0, len(date_forwards)-1)
                f1_points = date_forwards['Fantasy_Points'][a]
                date_forwards = date_forwards[date_forwards.index != a].reset_index().drop('level_0', axis = 1)

                b = randint(0, len(date_forwards)-1)
                f2_points = date_forwards['Fantasy_Points'][b]
                date_forwards = date_forwards[date_forwards.index != b].reset_index().drop('level_0', axis = 1)

                c = randint(0, len(date_midfielders)-1)
                m1_points = date_midfielders['Fantasy_Points'][c]
                date_midfielders = date_midfielders[date_midfielders.index != c].reset_index().drop('level_0', axis = 1)

                d = randint(0, len(date_midfielders)-1)
                m2_points = date_midfielders['Fantasy_Points'][d]
                date_midfielders = date_midfielders[date_midfielders.index != d].reset_index().drop('level_0', axis = 1)

                e = randint(0, len(date_defenders)-1)
                d1_points = date_defenders['Fantasy_Points'][e]
                date_defenders = date_defenders[date_defenders.index != e].reset_index().drop('level_0', axis = 1)

                f = randint(0, len(date_defenders)-1)
                d2_points = date_defenders['Fantasy_Points'][f]
                date_defenders = date_defenders[date_defenders.index != f].reset_index().drop('level_0', axis = 1)
                date_utilities = date_forwards.append(date_midfielders).append(date_defenders).reset_index().drop('level_0', axis= 1)


                g = randint(0, len(date_utilities)-1)
                u1_points = date_utilities['Fantasy_Points'][g]
                date_utilities = date_utilities[date_utilities.index != g].reset_index().drop('level_0', axis = 1)

                h = randint(0, len(date_utilities)-1)
                u2_points = date_utilities['Fantasy_Points'][h]


                i = randint(0, len(date_goalies)-1)
                g_points = date_goalies['Fantasy_Points'][i]

                lineup_points = f1_points + f2_points + m1_points + m2_points + d1_points + d2_points + u1_points+ u2_points + g_points

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

                writer.writerow(data)


if __name__ == "__main__":
    main()
