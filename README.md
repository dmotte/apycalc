# apycalc

TODO content

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
