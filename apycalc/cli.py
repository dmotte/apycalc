#!/usr/bin/env python3

import argparse
import csv
import statistics
import sys

from datetime import datetime as dt
from datetime import timedelta
from typing import TextIO


def load_data(file: TextIO, kvalue: str = 'Open') -> list[dict]:
    '''
    Loads data from a CSV file.

    Compatible with Yahoo Finance OHLCV CSV files, in particular
    https://github.com/dmotte/misc/blob/main/python-scripts/ohlcv-fetchers/yahoo-finance.py
    '''
    data = list(csv.DictReader(file))

    # Customize data structure
    data2 = []
    for x in data:
        y = {}
        y['date'] = dt.strptime(x['Date'], '%Y-%m-%d').date()
        y['value'] = float(x[kvalue])
        data2.append(y)

    return data2


def save_data(data: list[dict], file: TextIO):
    '''
    Saves data into a CSV file
    '''
    print('Date,Value,APY,APYMA', file=file)

    for entry in data:
        print(
            ','.join(
                entry['date'],
                entry['value'],
                entry['apy'],
                entry['apyma']),
            file=file)


def compute_stats(data_in: list[dict], window: int = 50) -> list[dict]:
    '''
    Computes APYs and Moving Averages
    '''
    data_out = []

    for index, entry in enumerate(data_in):
        # Get all entries which are at least 1 year older than the current one
        date_1yago = entry['date'] - timedelta(days=365)
        entries_1yago = [x for x in data_in if x['date'] <= date_1yago]

        if len(entries_1yago) == 0:
            continue

        # Calculate APY
        entry_1yago = entries_1yago[-1]
        entry['apy'] = entry['value'] / entry_1yago['value'] - 1

        # Calculate the Moving Average
        entries_ma = [x for i, x in enumerate(data_in)
                      if 'apy' in x
                      and i <= index
                      and i > index - window]
        entry['apyma'] = statistics.mean([x['apy'] for x in entries_ma])

    return data_out


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='APY trend calculator with configurable Moving Average'
    )

    parser.add_argument('file_in', metavar='FILE_IN', type=str,
                        nargs='?', default='-',
                        help='Input file. If set to "-" then stdin is used '
                        '(default: -)')
    parser.add_argument('file_out', metavar='FILE_OUT', type=str,
                        nargs='?', default='-',
                        help='Output file. If set to "-" then stdout is used '
                        '(default: -)')

    parser.add_argument('-k', '--kvalue', type=str, default='Open',
                        help='Column name of the asset values '
                        '(default: "Open")')

    parser.add_argument('-w', '--window', type=int, default=50,
                        help='Time window (number of entries) for the Moving '
                        'Average (default: 50)')

    args = parser.parse_args(argv[1:])

    ############################################################################

    if args.file_in == '-':
        data_in = load_data(sys.stdin, args.kvalue)
    else:
        with open(args.file_in, 'r') as f:
            data_in = load_data(f, args.kvalue)

    data_out = compute_stats(data_in, args.window)

    if args.file_out == '-':
        save_data(data_out, sys.stdout)
    else:
        with open(args.file_out, 'w') as f:
            save_data(data_out, f)

    return 0
