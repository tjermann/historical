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

Boxscores_DATA = 'boxscores/nfl_players.csv'
Team_Boxscores_DATA = 'boxscores/nfl_teams.csv'

csvfile = open('optimals/nfl_optimal_lineups.csv', 'w')
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

    quarterbacks = games[games.Position == 'QB'].sort('Fantasy_Points')
    runningbacks = games[games.Position == 'RB'].sort('Fantasy_Points')
    widereceivers = games[games.Position =='WR'].sort('Fantasy_Points')
    tightends = games[games.Position == 'TE'].sort('Fantasy_Points')
    defense = teams.sort('Fantasy_Points')
    

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

        date_quarterbacks = quarterbacks[quarterbacks.Date >= date][quarterbacks.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()
        date_runningbacks = runningbacks[runningbacks.Date >= date][runningbacks.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()
        date_widereceivers = widereceivers[widereceivers.Date >= date][widereceivers.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()
        date_tightends = tightends[tightends.Date >= date][tightends.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()
        date_defense = defense[defense.Date >= date][defense.Date <= end_week].sort('Fantasy_Points', ascending=False).reset_index()

        qb_points = round(date_quarterbacks['Fantasy_Points'][0],1)
        r1_points = round(date_runningbacks['Fantasy_Points'][0],1)
        r2_points = round(date_runningbacks['Fantasy_Points'][1],1)
        w1_points = round(date_widereceivers['Fantasy_Points'][0],1)
        w2_points = round(date_widereceivers['Fantasy_Points'][1],1)
        w3_points = round(date_widereceivers['Fantasy_Points'][2],1)
        te_points = round(date_tightends['Fantasy_Points'][0],1)
        u_points = round(max(date_runningbacks['Fantasy_Points'][2], date_widereceivers['Fantasy_Points'][3], date_tightends['Fantasy_Points'][1]),1)
        d_points = date_defense['Fantasy_Points'][0]

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

        if len(games) > 5:
            writer.writerow(data)


if __name__ == "__main__":
    main()
