#!/usr/bin/env python3

import argparse
import csv
import sys

from datetime import datetime as dt
from typing import TextIO

import plotly.express as px


def load_data(file: TextIO) -> list[dict]:
    '''
    Loads data from a CSV file
    '''
    data = list(csv.DictReader(file))

    # Customize data structure
    data2 = []
    for x in data:
        y = {}
        y['date'] = dt.strptime(x['Date'], '%Y-%m-%d').date()
        y['rate'] = float(x['Rate'])
        y['apy'] = float(x['APY'])
        y['apyma'] = float(x['APYMA'])
        data2.append(y)

    return data2


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Generate line plots based on asset rate and/or APY values'
    )

    parser.add_argument('file_in', metavar='FILE_IN', type=str,
                        nargs='?', default='-',
                        help='Input file. If set to "-" then stdin is used '
                        '(default: -)')

    parser.add_argument('-r', '--plot-rate', action='store_true',
                        help='Generate plot based on rates')
    parser.add_argument('-a', '--plot-apy', action='store_true',
                        help='Generate plot based on APYs and APYMAs')

    args = parser.parse_args(argv[1:])

    ############################################################################

    if args.file_in == '-':
        data = load_data(sys.stdin)
    else:
        with open(args.file_in, 'r') as f:
            data = load_data(f)

    if args.plot_rate:
        fig = px.line(
            data,
            x='date',
            y='rate',
            template='plotly_dark',
            title='Asset rate',
        )
        fig.show()

    if args.plot_apy:
        fig = px.line(
            data,
            x='date',
            y=['apy', 'apyma'],
            template='plotly_dark',
            title='APY and Moving Average',
        )
        fig.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
