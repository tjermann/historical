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

Boxscores_DATA = 'boxscores/nba_players.csv'
Players_DATA = 'positions/nba_positions.csv'

csvfile = open('optimals/nba_optimal_lineups.csv', 'w')
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
    games = games[games.Fantasy_Points > 0].sort('Fantasy_Points')

    guards = games[games.Position.isin(['G','SG','PG'])].sort('Fantasy_Points')
    forwards = games[games.Position.isin(['F','PF','SF'])].sort('Fantasy_Points')
    centers = games[games.Position =='C'].sort('Fantasy_Points')
    
    dates = games['Date'].unique()
    dates.sort()
    for i in range(0,len(dates)):
        #Contest will only be run on Single Days when there are 5 or more games available.
        date = dates[i]
        gameids = games[games.Date == date]['GameID'].unique()

        try:

            date_guards = guards[guards.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_forwards = forwards[forwards.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_centers = centers[centers.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
            date_utilities = [date_guards['Fantasy_Points'][3], date_guards['Fantasy_Points'][4], date_forwards['Fantasy_Points'][3], date_forwards['Fantasy_Points'][4], date_centers['Fantasy_Points'][1], date_centers['Fantasy_Points'][2]]
            date_utilities.sort(reverse=True)
        

            g1_points = round(date_guards['Fantasy_Points'][0],1)
            g2_points = round(date_guards['Fantasy_Points'][1],1)
            g3_points = round(date_guards['Fantasy_Points'][2],1)
            f1_points = round(date_forwards['Fantasy_Points'][0],1)
            f2_points = round(date_forwards['Fantasy_Points'][1],1)
            f3_points = round(date_forwards['Fantasy_Points'][2],1)
            c_points = round(date_centers['Fantasy_Points'][0],1)
            u1_points = round(date_utilities[0],1)
            u2_points = round(date_utilities[1],1)
 
            lineup_points = round(g1_points + g2_points+ g3_points + f1_points + f2_points + f3_points + c_points + u1_points + u2_points,1)

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

            if len(gameids) >= 5:
                writer.writerow(data)

        except Exception:
            continue


if __name__ == "__main__":
    main()
