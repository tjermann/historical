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

Boxscores_DATA = 'boxscores/nfl_players.csv'
Team_Boxscores_DATA = 'boxscores/nfl_teams.csv'

csvfile = open('lineups/nfl_lineups.csv', 'w')
fieldnames = ['Date','QB','RB1','RB2','WR1','WR2','WR3','TE','UTIL','D','Total']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    games = pandas.read_csv(Boxscores_DATA)
    teams = pandas.read_csv(Team_Boxscores_DATA)

    games_fields = ['Date',
                    'GameID',
                    'PlayerName',
                    'Position',
                    'Fantasy_Points']
    games = games[games_fields]
    games = games[games.Fantasy_Points > 0]
    teams = teams[teams.Fantasy_Points > 0]

    quarterbacks = games[games.Position == 'QB'].sort('Fantasy_Points')
    quarterbacks = quarterbacks[int(0.25*len(quarterbacks)):]
    runningbacks = games[games.Position == 'RB'].sort('Fantasy_Points')
    runningbacks = runningbacks[int(0.25*len(runningbacks)):]
    widereceivers = games[games.Position =='WR'].sort('Fantasy_Points')
    widereceivers = widereceivers[int(0.25*len(widereceivers)):]
    tightends = games[games.Position == 'TE'].sort('Fantasy_Points')
    tightends = tightends[int(0.25*len(tightends)):]
    defense = teams.sort('Fantasy_Points')
    defense = defense[int(0.25*len(defense)):]

    dates = games['Date'].unique()
    dates.sort()
    for i in range(0,len(dates)):
        #3 Consecutive games are used at a time cover Thursday-Monday situations, this will often overestimate the points scored due to taking Sunday to Sunday, however it will provide a conservative look rather than blocking out dates.
        date = dates[i]
        try:
            end_week = dates[i+2]
            gameids = games[games.Date >= date][games.Date <= end_week]['GameID'].unique()
        except Exception:
            gameids = games[games.Date == date]['GameID'].unique()
        if len(gameids) >5:
            for j in range(0, num_lineups):

                date_quarterbacks = quarterbacks[quarterbacks.Date >= date][quarterbacks.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()
                date_runningbacks = runningbacks[runningbacks.Date >= date][runningbacks.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()
                date_widereceivers = widereceivers[widereceivers.Date >= date][widereceivers.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()
                date_tightends = tightends[tightends.Date >= date][tightends.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()
                date_defense = defense[defense.Date >= date][defense.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()

                a = randint(0, len(date_quarterbacks)-1)
                qb_points = round(date_quarterbacks['Fantasy_Points'][a],1)

                b = randint(0, len(date_runningbacks)-1)
                r1_points = round(date_runningbacks['Fantasy_Points'][b],1)
                date_runningbacks = date_runningbacks[date_runningbacks.index != b].reset_index().drop('level_0', axis = 1)

                c = randint(0, len(date_runningbacks)-1)
                r2_points = round(date_runningbacks['Fantasy_Points'][c],1)
                date_runningbacks = date_runningbacks[date_runningbacks.index != c].reset_index().drop('level_0', axis = 1)

                d = randint(0, len(date_widereceivers)-1)
                w1_points = round(date_widereceivers['Fantasy_Points'][d],1)
                date_widereceivers = date_widereceivers[date_widereceivers.index != d].reset_index().drop('level_0', axis = 1)

                e = randint(0, len(date_widereceivers)-1)
                w2_points = round(date_widereceivers['Fantasy_Points'][e],1)
                date_widereceivers = date_widereceivers[date_widereceivers.index != e].reset_index().drop('level_0', axis = 1)

                f = randint(0, len(date_widereceivers)-1)
                w3_points = round(date_widereceivers['Fantasy_Points'][f],1)
                date_widereceivers = date_widereceivers[date_widereceivers.index != f].reset_index().drop('level_0', axis = 1)

                g = randint(0, len(date_tightends)-1)
                te_points = round(date_tightends['Fantasy_Points'][g],1)
                date_tightends = date_tightends[date_tightends.index != g].reset_index().drop('level_0', axis = 1)
                date_utilities = date_runningbacks.append(date_widereceivers).append(date_tightends).reset_index().drop('level_0', axis = 1)

                h = randint(0, len(date_utilities)-1)
                u_points = round(date_utilities['Fantasy_Points'][h],1)

                i = randint(0, len(date_defense)-1)
                d_points = round(date_defense['Fantasy_Points'][i],1)

                lineup_points = round(qb_points + r1_points + r2_points + w1_points + w2_points + w3_points + te_points + u_points + d_points,1)

                data = {'Date': date,
                        'QB': qb_points,
                        'RB1': r1_points,
                        'RB2': r2_points,
                        'WR1': w1_points,
                        'WR2': w2_points,
                        'WR3': w3_points,
                        'TE': te_points,
                        'UTIL': u_points,
                        'D': d_points,
                        'Total': lineup_points}


                writer.writerow(data)


if __name__ == "__main__":
    main()
