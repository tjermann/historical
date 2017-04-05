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

csvfile = open('optimals/ncaaf_optimal_lineups.csv', 'w')
fieldnames = ['Date','QB1','QB2','RB1','RB2','WR1','WR2','WR3','TE','UTIL','Total']
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

            qb1_points = round(date_quarterbacks['Fantasy_Points'][0],1)
            qb2_points = round(date_quarterbacks['Fantasy_Points'][1],1)
            r1_points = round(date_runningbacks['Fantasy_Points'][0],1)
            r2_points = round(date_runningbacks['Fantasy_Points'][1],1)
            w1_points = round(date_widereceivers['Fantasy_Points'][0],1)
            w2_points = round(date_widereceivers['Fantasy_Points'][1],1)
            w3_points = round(date_widereceivers['Fantasy_Points'][2],1)
            te_points = round(date_tightends['Fantasy_Points'][0],1)
            u_points = round(max(date_runningbacks['Fantasy_Points'][2], date_widereceivers['Fantasy_Points'][3], date_tightends['Fantasy_Points'][1]),1)
 
            lineup_points = round(qb1_points + qb2_points+ r1_points + r2_points + w1_points + w2_points + w3_points + te_points + u_points,1)

            data = {'Date': date,
                    'QB1': qb1_points,
                    'QB2': qb2_points,
                    'RB1': r1_points,
                    'RB2': r2_points,
                    'WR1': w1_points,
                    'WR2': w2_points,
                    'WR3': w3_points,
                    'TE': te_points,
                    'UTIL': u_points,
                    'Total': lineup_points}

            if len(gameids) >= 5:
                writer.writerow(data)

        except Exception:
            continue


if __name__ == "__main__":
    main()
