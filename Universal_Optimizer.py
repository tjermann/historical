from pandas import * 
import pandasql
import numpy as np
import MySQLdb as mdb
import sys
import string
import pdb
import datetime

class LineupOptimizer(object):
    def __init__(self,
                 input_data, 
                 positions,
                 dollars,
                 dollar_range,
                 lineups,
                 year, 
                 month, 
                 day, 
                 strategy=None,
                 backtest=False):
  
        self.data = input_data
        self.year = year
        self.month = month
        self.day = day
        self.positions = positions
        self.lineups = lineups
        self.dollars = dollars
        self.dollar_range = dollar_range
        self.strategy = None
        self.backtest = backtest

    def _prune_list(self, combined_df):
        combined_df = combined_df.dropna()
        combined_df.sort(['Points', 'Dollars'], 
                         ascending=[False, True],
                         inplace = True)

        combined_df['Duplicates'] = combined_df['Points'].shift()
        msk = combined_df['Points'] != combined_df['Duplicates']
        combined_df = combined_df.loc[msk]
        combined_df.drop(['Duplicates'], inplace=True, axis=1)

        combined_df.sort(['Dollars', 'Points'], 
                         ascending=[True, False],
                         inplace = True)

        combined_df['Duplicates'] = combined_df['Dollars'].shift()
        msk = combined_df['Dollars'] != combined_df['Duplicates']
        combined_df = combined_df.loc[msk]
        combined_df.drop(['Duplicates'], inplace=True, axis=1)

        combined_df.sort('Points', ascending=False, inplace=True)

        return combined_df

    def calc_lineup(self):
        points = self.data
        day = self.day
        month = self.month
        year = self.year
        positions = self.positions
        lineups = self.lineups
 
        for position in positions:
            try:
                all_dfs
                all_dfs.append(self.filter_and_rename(points, position, position))
            except Exception:
                all_dfs = [self.filter_and_rename(points, position, position)]

            combined_df = all_dfs[0]

        for i in range(0, len(positions)-1): 
            j = i+1

            combined_df = combined_df.merge(all_dfs[j])
            pos1 = positions[i]
            pos2 = positions[j]

            combined_df = combined_df.merge(all_dfs[i])

            if i == 0:
                combined_df['Dollars'] = (combined_df['Dollars_'+ pos1] +
                                          combined_df['Dollars_'+ pos2])
                combined_df['Points'] = (combined_df['Points_' + pos1] +
                                         combined_df['Points_'+ pos2])

            else:
                combined_df['Dollars'] = (combined_df['Dollars'] +
                                          combined_df['Dollars_'+ pos2])
                combined_df['Points'] = (combined_df['Points'] +
                                         combined_df['Points_'+ pos2])

            combined_df.drop(['Position_'+ pos1,
                              'Dollars_'+ pos1,
                              'Points_'+ pos1,
                              'Position_'+ pos2,
                              'Dollars_'+ pos2,
                              'Points_'+ pos2], inplace=True, axis=1)
         
            for x in range (0, j):
                pos1 = positions[x]
                pos2 = positions[j]
                combined_df = combined_df[combined_df['Player_ID_'+ pos1] != combined_df['Player_ID_'+ pos2]]

            combined_df = self._prune_list(combined_df)

        # Remove Expensive and sort
        combined_df = combined_df[combined_df['Dollars'] <= self.dollars]
        combined_df = combined_df[combined_df['Dollars'] >= int(self.dollars) - int(self.dollar_range)]

        combined_df=combined_df.reset_index()
        combined_df['Unique'] = None
        combined_df = combined_df.drop('Unique',1)
        combined_df = combined_df.drop('index',1)
        combined_df = combined_df.drop('join_key',1)

        combined_df.sort('Points', 
                         ascending= False,
                         inplace = True)

        combined_df = combined_df.head(lineups)
        return combined_df

    def filter_and_rename(self, df, position, append=None):
        if position in ('G'):
            ret_df = df[df['Position'] == 'G']

        if position in ('F1','F2'):
            ret_df = df[df['Position'] == 'F']

        if position in ('M1','M2'):
            ret_df = df[df['Position'] == 'M']

        if position in ('D1','D2'):
            ret_df = df[df['Position'] == 'D']

        if position in ('U1','U2'):
            ret_df = df[df['Position'].isin(['F','M','D'])]

        ret_df['join_key'] = 1
        ret_df = ret_df.rename(columns={'Position': 'Position_' + append,
                                        'PlayerID': 'Player_ID_' + append,
                                        'Points': 'Points_' + append,
                                        'Dollars': 'Dollars_' + append})

        return ret_df

