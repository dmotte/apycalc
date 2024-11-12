#!/bin/bash

set -e

# Local path to the https://github.com/dmotte/misc/blob/main/python-scripts/ohlcv-fetchers/yahoo-finance.py script
readonly fetcher=${1:?}

readonly symbol=${2:?} dt_start=${3:-1970-01-01T00Z}

if [[ "$(uname)" = MINGW* ]]
    then py=$(dirname "$fetcher")/venv/Scripts/python
    else py=$(dirname "$fetcher")/venv/bin/python3
fi

# We separately invoke the fetcher script in advance, to avoid masking its
# return value
data=$("$py" "$fetcher" "$symbol" -i1wk -d"$dt_start" -f'{:.6f}')
echo "$data" | tr -d '\r'
