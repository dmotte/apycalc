#!/bin/bash

set -e

readonly fetcher= # TODO path to misc/python-scripts/ohlcv-fetchers/yahoo-finance.py (pass it as first arg)

symbol=${1:?}

if [[ "$(uname)" = MINGW* ]]
    then py=$(dirname "$fetcher")/venv/Scripts/python
    else py=$(dirname "$fetcher")/venv/bin/python3
fi

# TODO customizable datetime as arg
"$py" "$fetcher" "$symbol" -i1wk -d1970-01-01T00Z -f'{:.6f}' | tr -d '\r'
