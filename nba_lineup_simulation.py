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
num_lineups = 10

Boxscores_DATA = 'boxscores/nba_players.csv'
Players_DATA = 'positions/nba_positions.csv'

csvfile = open('lineups/nba_lineups.csv', 'w')
fieldnames = ['Date','G1','G2','G3','F1','F2','F3','C','U1','U2','Total']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    games = pandas.read_csv(Boxscores_DATA)
    players = pandas.read_csv(Players_DATA)

    games = games[['Year','Date','GameID','PlayerName','Fantasy_Points']]

    games = merge(games, players, on=['Year','PlayerName'], how='left')

    games_fields = ['Date',
                    'GameID',
                    'PlayerName',
                    'Position',
                    'Fantasy_Points']
    games = games[games_fields]
    games = games[games.Fantasy_Points > 0]

    guards = games[games.Position.isin(['G','SG','PG'])].sort('Fantasy_Points')
    guards = guards[int(0.25*len(guards)):]
    forwards = games[games.Position.isin(['F','SF','PF'])].sort('Fantasy_Points')
    forwards = forwards[int(0.25*len(forwards)):] 
    centers = games[games.Position =='C'].sort('Fantasy_Points')
    centers = centers[int(0.25*len(centers)):]
    utilities = games.sort('Fantasy_Points')
    utilities = utilities[int(0.25*len(utilities)):]
    

    dates = games['Date'].unique()
    dates.sort()
    for date in dates:
        gameids = games[games.Date == date]['GameID'].unique()
        try:
            for j in range(0, num_lineups):

                date_guards = guards[guards.Date == date].reset_index()
                date_forwards = forwards[forwards.Date == date].reset_index()
                date_centers = centers[centers.Date == date].reset_index()

                a = randint(0, len(date_guards)-1)
                g1_points = date_guards['Fantasy_Points'][a]
                date_guards = date_guards[date_guards.index != a].reset_index().drop('level_0', axis = 1)

                b = randint(0, len(date_guards)-1)
                g2_points = date_guards['Fantasy_Points'][b]
                date_guards = date_guards[date_guards.index != b].reset_index().drop('level_0', axis = 1)

                c = randint(0, len(date_guards)-1)
                g3_points = date_guards['Fantasy_Points'][c]
                date_guards = date_guards[date_guards.index != c].reset_index().drop('level_0', axis = 1)

                d = randint(0, len(date_forwards)-1)
                f1_points = date_forwards['Fantasy_Points'][d]
                date_forwards = date_forwards[date_forwards.index != d].reset_index().drop('level_0', axis = 1)

                e = randint(0, len(date_forwards)-1)
                f2_points = date_forwards['Fantasy_Points'][e]
                date_forwards = date_forwards[date_forwards.index != e].reset_index().drop('level_0', axis = 1)

                f = randint(0, len(date_forwards)-1)
                f3_points = date_forwards['Fantasy_Points'][f]
                date_forwards = date_forwards[date_forwards.index != f].reset_index().drop('level_0', axis = 1)

                g = randint(0, len(date_centers)-1)
                c_points = date_centers['Fantasy_Points'][g]
                date_centers = date_centers[date_centers.index != g].reset_index().drop('level_0', axis = 1)
                date_utilities = date_guards.append(date_forwards).append(date_centers).reset_index().drop('level_0', axis = 1)

                h = randint(0, len(date_utilities)-1)
                u1_points = date_utilities['Fantasy_Points'][h]
                date_utilities = date_utilities[date_utilities.index != h].reset_index().drop('level_0', axis = 1)

                i = randint(0, len(date_utilities)-1)
                u2_points = date_utilities['Fantasy_Points'][i]

                lineup_points = g1_points + g2_points + g3_points + f1_points + f2_points + f3_points + c_points+ u1_points + u2_points

                data = {'Date': date,
                        'G1': g1_points,
                        'G2': g2_points,
                        'G3': g3_points,
                        'F1': f1_points,
                        'F2': f2_points,
                        'F3': f3_points,
                        'C': c_points,
                        'U1': u1_points,
                        'U2': u2_points,
                        'Total': lineup_points}

                if len(gameids) >5:

                    writer.writerow(data)

        except Exception:
            pass


if __name__ == "__main__":
    main()
