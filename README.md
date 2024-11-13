# apycalc

TODO content

TODO test `cli.py` thoroughly

```bash
# TODO
cd example/

python3 -mvenv venv
venv/bin/python3 -mpip install -r requirements.txt

# TODO write to customize path to the fetcher
./fetch.sh ~/git/misc/python-scripts/ohlcv-fetchers/yahoo-finance.py '^GSPC' 2000-01-01T00Z > ohlcv-SPX500.csv
python3 -mapycalc -w104 -f'{:.6f}' < ohlcv-SPX500.csv > apy-SPX500.csv
venv/bin/python3 plots.py -ra < apy-SPX500.csv
```
