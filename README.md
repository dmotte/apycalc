# apycalc

TODO content

TODO test `cli.py` thoroughly
TODO test `example/plots.py` thoroughly

```bash
# TODO
cd example/

python3 -mvenv venv
venv/bin/python3 -mpip install -r requirements.txt

# TODO write to customize path to the fetcher
./fetch.sh ~/git/misc/python-scripts/ohlcv-fetchers/yahoo-finance.py '^GSPC' 2000-01-01T00Z > SPX500.csv
python3 -mapycalc --help TODO | venv/bin/python3 plots.py -ra
```
