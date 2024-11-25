#!/usr/bin/env python3

import io
import textwrap

from datetime import date

from apycalc import load_data, save_data


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


def test_save_data():
    data = [
        {'date': date(2000, 1, 1), 'rate': 11, 'apy': 0.12, 'apyma': 0.13},
        {'date': date(2000, 1, 2), 'rate': 21, 'apy': 0.22, 'apyma': 0.23},
        {'date': date(2000, 1, 3), 'rate': 31, 'apy': 0.32, 'apyma': 0.33},
    ]

    csv = textwrap.dedent('''\
        Date,Rate,APY,APYMA
        2000-01-01,11,0.12,0.13
        2000-01-02,21,0.22,0.23
        2000-01-03,31,0.32,0.33
    ''')

    buf = io.StringIO()
    save_data(data, buf)
    buf.seek(0)

    assert buf.read() == csv

    csv = textwrap.dedent('''\
        Date,Rate,APY,APYMA
        2000-01-01,11.000,0.12,0.13
        2000-01-02,21.000,0.22,0.23
        2000-01-03,31.000,0.32,0.33
    ''')

    buf = io.StringIO()
    save_data(data, buf, fmt_rate='{:.3f}')
    buf.seek(0)

    assert buf.read() == csv

    csv = textwrap.dedent('''\
        Date,Rate,APY,APYMA
        2000-01-01,11,0.1200,0.1300
        2000-01-02,21,0.2200,0.2300
        2000-01-03,31,0.3200,0.3300
    ''')

    buf = io.StringIO()
    save_data(data, buf, fmt_yield='{:.4f}')
    buf.seek(0)

    assert buf.read() == csv
