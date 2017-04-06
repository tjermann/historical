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

Boxscores_DATA = 'boxscores/ncaaf_players.csv'
Players_DATA = 'positions/ncaaf_positions.csv'

csvfile = open('lineups/ncaaf_lineups.csv', 'w')
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
    quarterbacks = quarterbacks[int(0.25*len(quarterbacks)):]
    runningbacks = games[games.Position == 'RB'].sort('Fantasy_Points')
    runningbacks = runningbacks[int(0.25*len(runningbacks)):]
    widereceivers = games[games.Position =='WR'].sort('Fantasy_Points')
    widereceivers = widereceivers[int(0.25*len(widereceivers)):]
    tightends = games[games.Position == 'TE'].sort('Fantasy_Points')
    tightends = tightends[int(0.25*len(tightends)):]

    dates = games['Date'].unique()
    dates.sort()
    for i in range(0,len(dates)):
        #Contest will only be run on Single Days when there are 5 or more games available.
        date = dates[i]
        gameids = games[games.Date == date]['GameID'].unique()


        if len(gameids) >5:
            for j in range(0, num_lineups):

                date_quarterbacks = quarterbacks[quarterbacks.Date == date].reset_index()
                date_runningbacks = runningbacks[runningbacks.Date == date].reset_index()
                date_widereceivers = widereceivers[widereceivers.Date == date].reset_index()
                date_tightends = tightends[tightends.Date == date].reset_index()

                a = randint(0, len(date_quarterbacks)-1)
                qb1_points = round(date_quarterbacks['Fantasy_Points'][a],1)
                date_quarterbacks = date_quarterbacks[date_quarterbacks.index != a].reset_index().drop('level_0', axis = 1)

                b = randint(0, len(date_quarterbacks)-1)
                qb2_points = round(date_quarterbacks['Fantasy_Points'][b],1)

                c = randint(0, len(date_runningbacks)-1)
                r1_points = round(date_runningbacks['Fantasy_Points'][c],1)
                date_runningbacks = date_runningbacks[date_runningbacks.index != c].reset_index().drop('level_0', axis = 1)

                d = randint(0, len(date_runningbacks)-1)
                r2_points = round(date_runningbacks['Fantasy_Points'][d],1)
                date_runningbacks = date_runningbacks[date_runningbacks.index != d].reset_index().drop('level_0', axis = 1)

                e = randint(0, len(date_widereceivers)-1)
                w1_points = round(date_widereceivers['Fantasy_Points'][e],1)
                date_widereceivers = date_widereceivers[date_widereceivers.index != e].reset_index().drop('level_0', axis = 1)

                f = randint(0, len(date_widereceivers)-1)
                w2_points = round(date_widereceivers['Fantasy_Points'][f],1)
                date_widereceivers = date_widereceivers[date_widereceivers.index != f].reset_index().drop('level_0', axis = 1)

                g = randint(0, len(date_widereceivers)-1)
                w3_points = round(date_widereceivers['Fantasy_Points'][g],1)
                date_widereceivers = date_widereceivers[date_widereceivers.index != g].reset_index().drop('level_0', axis = 1)

                h = randint(0, len(date_tightends)-1)
                te_points = round(date_tightends['Fantasy_Points'][h],1)
                date_tightends = date_tightends[date_tightends.index != h].reset_index().drop('level_0', axis = 1)
                date_utilities = date_runningbacks.append(date_widereceivers).append(date_tightends).reset_index().drop('level_0', axis = 1)

                i = randint(0, len(date_utilities)-1)
                u_points = round(date_utilities['Fantasy_Points'][i],1)

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

                writer.writerow(data)

if __name__ == "__main__":
    main()
