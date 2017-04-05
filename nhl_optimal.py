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

csvfile = open('optimals/nhl_optimal_lineups.csv', 'w')
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
    games = games[games.Fantasy_Points > 0].sort('Fantasy_Points')
    goalies = goalies[games_fields]
    goalies = goalies[goalies.Fantasy_Points > 0].sort('Fantasy_Points')

    wings = games[games.Position.isin(['RW','LW'])].sort('Fantasy_Points')
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
            date_utilities = [date_wings['Fantasy_Points'][3], date_defenders['Fantasy_Points'][2], date_centers['Fantasy_Points'][2]]
            date_utilities.sort(reverse=True)
        

            w1_points = round(date_wings['Fantasy_Points'][0],1)
            w2_points = round(date_wings['Fantasy_Points'][1],1)
            w3_points = round(date_wings['Fantasy_Points'][2],1)
            c1_points = round(date_centers['Fantasy_Points'][0],1)
            c2_points = round(date_centers['Fantasy_Points'][1],1)
            d1_points = round(date_defenders['Fantasy_Points'][2],1)
            d2_points = round(date_defenders['Fantasy_Points'][0],1)
            u_points = round(date_utilities[0],1)
            g_points = round(date_goalies['Fantasy_Points'][0],1)
 
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

            if len(gameids) >= 5:
                writer.writerow(data)

        except Exception:
            continue


if __name__ == "__main__":
    main()
