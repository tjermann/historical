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

Boxscores_DATA = 'boxscores/nhl_players.csv'
Goalies_DATA = 'boxscores/nhl_goalies.csv'
Players_DATA = 'positions/nhl_positions.csv'

csvfile = open('lineups/nhl_lineups.csv', 'w')
fieldnames = ['Date','W1','W2','W3','C1','C2','D1','D2','U','G','Total']
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
    games = games[games.Fantasy_Points > 0]
    goalies = goalies[games_fields]
    goalies = goalies[goalies.Fantasy_Points > 0].sort('Fantasy_Points')

    wings = games[games.Position.isin(['RW','LW'])].sort('Fantasy_Points')
    wings = wings[int(0.25*len(wings)):]
    centers = games[games.Position == 'C'].sort('Fantasy_Points')
    centers = centers[int(0.25*len(centers)):]
    defenders = games[games.Position == 'D'].sort('Fantasy_Points')
    defenders = defenders[int(0.25*len(defenders)):]
    goalies = goalies[int(0.25*len(goalies)):]


    dates = games['Date'].unique()
    dates.sort()
    for date in dates:
        gameids = games[games.Date == date]['GameID'].unique()
        if len(gameids) >5:
            for j in range(0, num_lineups):

                date_wings = wings[wings.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
                date_defenders = defenders[defenders.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
                date_centers = centers[centers.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
                date_goalies = goalies[goalies.Date == date].sort('Fantasy_Points', ascending=False).reset_index()

                a = randint(0, len(date_wings)-1)
                w1_points = date_wings['Fantasy_Points'][a]
                date_wings = date_wings[date_wings.index != a].reset_index().drop('level_0', axis = 1)

                b = randint(0, len(date_wings)-1)
                w2_points = date_wings['Fantasy_Points'][b]
                date_wings = date_wings[date_wings.index != b].reset_index().drop('level_0', axis = 1)

                c = randint(0, len(date_wings)-1)
                w3_points = date_wings['Fantasy_Points'][c]
                date_wings = date_wings[date_wings.index != c].reset_index().drop('level_0', axis = 1)

                d = randint(0, len(date_centers)-1)
                c1_points = date_centers['Fantasy_Points'][d]
                date_centers = date_centers[date_centers.index != d].reset_index().drop('level_0', axis = 1)

                e = randint(0, len(date_centers)-1)
                c2_points = date_centers['Fantasy_Points'][e]
                date_centers = date_centers[date_centers.index != e].reset_index().drop('level_0', axis = 1)

                f = randint(0, len(date_defenders)-1)
                d1_points = date_defenders['Fantasy_Points'][f]
                date_defenders = date_defenders[date_defenders.index != f].reset_index().drop('level_0', axis = 1)

                g = randint(0, len(date_defenders)-1)
                d2_points = date_defenders['Fantasy_Points'][g]
                date_defenders = date_defenders[date_defenders.index != g].reset_index().drop('level_0', axis = 1)
                date_utilities = date_wings.append(date_centers).append(date_defenders).reset_index().drop('level_0', axis = 1)

                h = randint(0, len(date_utilities)-1)
                u_points = date_utilities['Fantasy_Points'][h]
                date_utilities = date_utilities[date_utilities.index != h].reset_index().drop('level_0', axis = 1)

                i = randint(0, len(date_goalies)-1)
                g_points = date_goalies['Fantasy_Points'][i]

                lineup_points = round(w1_points + w2_points+ w3_points + c1_points + c2_points + d1_points + d2_points + u_points + g_points,1)

                data = {'Date': date,
                        'W1': w1_points,
                        'W2': w2_points,
                        'W3': w3_points,
                        'C1': c1_points,
                        'C2': c2_points,
                        'D1': d1_points,
                        'D2': d2_points,
                        'U': u_points,
                        'G': g_points,
                        'Total': lineup_points}

                writer.writerow(data)


if __name__ == "__main__":
    main()
