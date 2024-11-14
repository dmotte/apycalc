# apycalc

[![GitHub main workflow](https://img.shields.io/github/actions/workflow/status/dmotte/apycalc/main.yml?branch=main&logo=github&label=main&style=flat-square)](https://github.com/dmotte/apycalc/actions)
[![PyPI](https://img.shields.io/pypi/v/apycalc?logo=python&style=flat-square)](https://pypi.org/project/apycalc/)

:snake: [**APY**](https://www.investopedia.com/terms/a/apy.asp) (_Annual Percentage Yield_) **trend calculator**, with configurable MA (_Moving Average_).

> **Note**: APY is calculated over a period of **365 days**.

## Installation

This utility is available as a Python package on **PyPI**:

```bash
pip3 install apycalc
```

## Usage

```bash
# TODO
cd example/

python3 -mvenv venv
venv/bin/python3 -mpip install -r requirements.txt

# TODO write to customize path to the invoke.sh script. It's essentially the local path to the https://github.com/dmotte/misc/blob/main/python-scripts/ohlcv-fetchers/invoke.sh script
~/git/misc/python-scripts/ohlcv-fetchers/invoke.sh yahoo-finance '^GSPC' -i1wk -d2000-01-01T00Z -f'{:.6f}' > ohlcv-SPX500.csv
python3 -mapycalc -w104 -f'{:.6f}' < ohlcv-SPX500.csv > apy-SPX500.csv
venv/bin/python3 plots.py -ra < apy-SPX500.csv
```

For more details on how to use this command, you can also refer to its help message (`--help`).

## Development

If you want to contribute to this project, you can install the package in **editable** mode:

```bash
pip3 install -e . --user
```

This will just link the package to the original location, basically meaning any changes to the original package would reflect directly in your environment ([source](https://stackoverflow.com/a/35064498)).
