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

Boxscores_DATA = 'boxscores/mlb_hitters.csv'
Pitchers_DATA = 'boxscores/mlb_pitchers.csv'

csvfile = open('lineups/mlb_lineups.csv', 'w')
fieldnames = ['Date','P','C','1B','2B','SS','3B','OF1','OF2','OF3','Total']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def main():
    games = pandas.read_csv(Boxscores_DATA)
    pitchers = pandas.read_csv(Pitchers_DATA)

    pitchers['Position'] = 'P'

    games_fields = ['Date',
                    'GameID',
                    'PlayerName',
                    'Position',
                    'Fantasy_Points']
    games = games[games_fields]
    games = games[games.Fantasy_Points > 0]
    pitchers = pitchers[games_fields]
    pitchers = pitchers[pitchers.Fantasy_Points > 0].sort('Fantasy_Points')

    catchers = games[games.Position == 'C'].sort('Fantasy_Points')
    catchers = catchers[int(0.25*len(catchers)):]
    firstbasemen = games[games.Position == '1B'].sort('Fantasy_Points')
    firstbasemen = firstbasemen[int(0.25*len(firstbasemen)):]
    secondbasemen = games[games.Position == '2B'].sort('Fantasy_Points')
    secondbasemen = secondbasemen[int(0.25*len(secondbasemen)):]
    shortstops = games[games.Position == 'SS'].sort('Fantasy_Points')
    shortstops = shortstops[int(0.25*len(shortstops)):]
    thirdbasemen = games[games.Position == '3B'].sort('Fantasy_Points')
    thirdbasemen = thirdbasemen[int(0.25*len(thirdbasemen)):]
    outfielders = games[games.Position.isin(['OF','DH','PH'])].sort('Fantasy_Points')
    outfielders = outfielders[int(0.25*len(outfielders)):]
    pitchers = pitchers.sort('Fantasy_Points')
    pitchers = pitchers[int(0.25*len(pitchers)):]

    dates = games['Date'].unique()
    dates.sort()
    for date in dates:
        gameids = games[games.Date == date]['GameID'].unique()
        if len(gameids) >5:
            for j in range(0, num_lineups):

                date_catchers = catchers[catchers.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
                date_firstbasemen = firstbasemen[firstbasemen.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
                date_secondbasemen = secondbasemen[secondbasemen.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
                date_shortstops = shortstops[shortstops.Date == date].sort('Fantasy_Points', ascending = False).reset_index()
                date_thirdbasemen = thirdbasemen[thirdbasemen.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
                date_outfielders = outfielders[outfielders.Date == date].sort('Fantasy_Points', ascending=False).reset_index()
                date_pitchers = pitchers[pitchers.Date == date].sort('Fantasy_Points', ascending=False).reset_index()

                a = randint(0, len(date_pitchers)-1)
                p_points = date_pitchers['Fantasy_Points'][a]

                b = randint(0, len(date_catchers)-1)
                c_points = date_catchers['Fantasy_Points'][b]
                date_catchers = date_catchers[date_catchers.index != b].reset_index().drop('level_0', axis = 1)

                c = randint(0, len(date_firstbasemen)-1)
                b1_points = date_firstbasemen['Fantasy_Points'][c]
                date_firstbasemen = date_firstbasemen[date_firstbasemen.index != c].reset_index().drop('level_0', axis = 1)

                d = randint(0, len(date_secondbasemen)-1)
                b2_points = date_secondbasemen['Fantasy_Points'][d]
                date_secondbasemen = date_secondbasemen[date_secondbasemen.index != d].reset_index().drop('level_0', axis = 1)

                e = randint(0, len(date_shortstops)-1)
                ss_points = date_shortstops['Fantasy_Points'][e]
                date_shortstops = date_shortstops[date_shortstops.index != e].reset_index().drop('level_0', axis = 1)

                f = randint(0, len(date_thirdbasemen)-1)
                b3_points = date_thirdbasemen['Fantasy_Points'][f]
                date_thirdbasemen = date_thirdbasemen[date_thirdbasemen.index != f].reset_index().drop('level_0', axis = 1)

                g = randint(0, len(date_outfielders)-1)
                of1_points = date_outfielders['Fantasy_Points'][g]
                date_outfielders = date_outfielders[date_outfielders.index != g].reset_index().drop('level_0', axis = 1)

                h = randint(0, len(date_outfielders)-1)
                of2_points = date_outfielders['Fantasy_Points'][h]
                date_outfielders = date_outfielders[date_outfielders.index != h].reset_index().drop('level_0', axis = 1)

                i = randint(0, len(date_outfielders)-1)
                of3_points = date_outfielders['Fantasy_Points'][i]

                lineup_points = round(p_points + c_points+ b1_points + b2_points + ss_points + b3_points + of1_points + of2_points +of3_points,1)

                data = {'Date': date,
                        'P': p_points,
                        'C': c_points,
                        '1B': b1_points,
                        '2B': b2_points,
                        'SS': ss_points,
                        '3B': b3_points,
                        'OF1': of1_points,
                        'OF2': of2_points,
                        'OF3': of3_points,
                        'Total': lineup_points}

                writer.writerow(data)


if __name__ == "__main__":
    main()
