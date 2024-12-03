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


def save_data(data: list[dict], file: TextIO, fmt_rate: str = '',
              fmt_yield: str = ''):
    '''
    Saves data into a CSV file
    '''
    func_rate = str if fmt_rate == '' else (lambda x: fmt_rate.format(x))
    func_yield = str if fmt_yield == '' else (lambda x: fmt_yield.format(x))

    fields = {
        'date': {
            'header': 'Date',
            'fmt': lambda x: dt.strftime(x, '%Y-%m-%d'),
        },
        'rate': {'header': 'Rate', 'fmt': func_rate},
        'apy': {'header': 'APY', 'fmt': func_yield},
        'apyma': {'header': 'APYMA', 'fmt': func_yield},
    }

    print(','.join(f['header'] for f in fields.values()), file=file)
    for x in data:
        print(','.join(f['fmt'](x[k]) for k, f in fields.items()), file=file)


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

    parser.add_argument('--fmt-rate', type=str, default='',
                        help='If specified, formats the rate values with this '
                        'format string (e.g. "{:.6f}")')
    parser.add_argument('--fmt-yield', type=str, default='',
                        help='If specified, formats the yield values with this '
                        'format string (e.g. "{:.4f}")')

    args = parser.parse_args(argv[1:])

    ############################################################################

    def lambda_read(file: TextIO):
        return load_data(file, args.krate)

    if args.file_in == '-':
        data_in = lambda_read(sys.stdin)
    else:
        with open(args.file_in, 'r') as f:
            data_in = lambda_read(f)

    data_out = compute_stats(data_in, args.window)

    def lambda_write(data: list[dict], file: TextIO):
        return save_data(data, file, args.fmt_rate, args.fmt_yield)

    if args.file_out == '-':
        lambda_write(data_out, sys.stdout)
    else:
        with open(args.file_out, 'w') as f:
            lambda_write(data_out, f)

    return 0
