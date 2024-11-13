#!/usr/bin/env python3

import argparse
import csv
import statistics
import sys

from datetime import datetime as dt
from datetime import timedelta
from typing import TextIO


def load_data(file: TextIO, krate: str = 'Open') -> list[dict]:
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
        y['rate'] = float(x[krate])
        data2.append(y)

    return data2


def save_data(data: list[dict], file: TextIO, fmt: str = ''):
    '''
    Saves data into a CSV file
    '''
    data = [x.copy() for x in data]

    if fmt != '':
        for x in data:
            for i, v in x.items():
                if isinstance(v, float):
                    x[i] = fmt.format(v)

    print('Date,Rate,APY,APYMA', file=file)

    for x in data:
        print('%s,%s,%s,%s' % (dt.strftime(x['date'], '%Y-%m-%d'),
                               x['rate'], x['apy'], x['apyma']), file=file)


def get_entry_1yago(data: list[dict], index: int) -> dict:
    '''
    Returns the entry that is one year (365 days) before the one whose index is
    passed as a parameter.

    Warning: it assumes that the entries are sorted by date in ascending order!
    '''
    date_1yago = data[index]['date'] - timedelta(days=365)

    for i in range(index - 1, -1, -1):
        if data[i]['date'] <= date_1yago:
            return data[i]

    return None


def compute_stats(data: list[dict], window: int = 50):
    '''
    Computes APYs and Moving Averages
    '''
    data = [x.copy() for x in data]

    for index, entry in enumerate(data):
        entry_1yago = get_entry_1yago(data, index)
        if entry_1yago is None:
            continue

        entry['apy'] = entry['rate'] / entry_1yago['rate'] - 1

        entries_ma = [x for i, x in enumerate(data)
                      if 'apy' in x
                      and i > index - window and i <= index]
        entry['apyma'] = statistics.mean(x['apy'] for x in entries_ma)

        yield entry


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

    parser.add_argument('-k', '--krate', type=str, default='Open',
                        help='Column name for the asset rate values '
                        '(default: "Open")')

    parser.add_argument('-w', '--window', type=int, default=50,
                        help='Time window (number of entries) for the Moving '
                        'Average (default: 50)')

    parser.add_argument('-f', '--format', type=str, default='',
                        help='If specified, formats the float values (such as '
                        'APYs and Moving Averages) with this format string '
                        '(e.g. "{:.6f}")')

    args = parser.parse_args(argv[1:])

    ############################################################################

    if args.file_in == '-':
        data_in = load_data(sys.stdin, args.krate)
    else:
        with open(args.file_in, 'r') as f:
            data_in = load_data(f, args.krate)

    data_out = compute_stats(data_in, args.window)

    if args.file_out == '-':
        save_data(data_out, sys.stdout, args.format)
    else:
        with open(args.file_out, 'w') as f:
            save_data(data_out, f, args.format)

    return 0
