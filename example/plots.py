#!/usr/bin/env python3

import argparse
import csv
import sys

from collections.abc import Iterator
from contextlib import ExitStack
from datetime import datetime as dt
from typing import Any, TextIO

import plotly.express as px


def load_data(file: TextIO) -> Iterator[dict[str, Any]]:
    '''
    Loads data from a CSV file
    '''
    data = list(csv.DictReader(file))

    for x in data:
        yield {
            'date': dt.strptime(x['Date'], '%Y-%m-%d').date(),
            'rate': float(x['Rate']),
            'apy': float(x['APY']),
            'apyma': float(x['APYMA']),
        }


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Generate plots based on data computed with apycalc'
    )

    parser.add_argument('file_in', metavar='FILE_IN', type=str,
                        nargs='?', default='-',
                        help='Input file. If set to "-" then stdin is used '
                        '(default: %(default)s)')

    parser.add_argument('-r', '--plot-rate', action='store_true',
                        help='Generate plot based on rate values')
    parser.add_argument('-a', '--plot-apy', action='store_true',
                        help='Generate plot based on APY values')

    args = parser.parse_args(argv[1:])

    ############################################################################

    with ExitStack() as stack:
        file_in = (sys.stdin if args.file_in == '-'
                   else stack.enter_context(open(args.file_in, 'r')))
        data = list(load_data(file_in))

    if args.plot_rate:
        fig = px.line(
            data,
            x='date',
            y='rate',
            template='plotly_dark',
            title=f'Rate values: {args.file_in}',
        )
        fig.show()

    if args.plot_apy:
        fig = px.line(
            data,
            x='date',
            y=['apy', 'apyma'],
            template='plotly_dark',
            title=f'APY values: {args.file_in}',
        )
        fig.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
