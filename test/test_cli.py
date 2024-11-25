#!/usr/bin/env python3

import io
import textwrap

from datetime import date

from apycalc import load_data


def test_load_data():
    csv = textwrap.dedent('''\
        Date,Open,High,Low,Close,Adj Close,Volume
        2000-01-01,10,15,9,12,12,123
        2000-01-08,12,13.5,10.2,13,13,456
        2000-01-15,13,22.1,13,18.5,18,789
    ''')

    data = load_data(io.StringIO(csv))

    assert data[0] == {'date': date(2000, 1, 1), 'rate': 10}
    assert data[1] == {'date': date(2000, 1, 8), 'rate': 12}
    assert data[2] == {'date': date(2000, 1, 15), 'rate': 13}

    data = load_data(io.StringIO(csv), krate='Close')

    assert data[0] == {'date': date(2000, 1, 1), 'rate': 12}
    assert data[1] == {'date': date(2000, 1, 8), 'rate': 13}
    assert data[2] == {'date': date(2000, 1, 15), 'rate': 18.5}
