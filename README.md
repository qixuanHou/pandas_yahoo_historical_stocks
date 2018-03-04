# pandas_yahoo_historical_stocks
Python wrapper for collecting historical stock prices and dividends through yahoo finance and returning them in a pandas dataframe.

**needed packages: 
`requests
datetime
json
pandas`**

```
# Either copy historical_prices_and_dividends.py into your code base:
import historical_prices_and_dividends

# Or call as package:
#from pandas_yahoo_historical_stocks import historical_prices_and_dividends

'''Get IBM's stock prices for 2017/1/1 - current date'''
df_stocks = historical_prices_and_dividends.get_historical_prices(ticker="IBM",
                                                                 start_date=datetime.datetime(2017,1,1),
                                                                 end_date=datetime.datetime.now())
                                                                 
'''Get IBM's dividends  for 2017/1/1 - current date'''
df_dividends = historical_prices_and_dividends.get_historical_dividends(ticker="IBM",
                                                                 start_date=datetime.datetime(2017,1,1),
                                                                 end_date=datetime.datetime.now())



df_stocks.head()

'''head call output:
adjclose	close	date	high	low	open	volume
0	154.490005	154.490005	2018-03-02	154.759995	151.880005	152.789993	3261141
1	153.809998	153.809998	2018-03-01	156.970001	152.789993	155.529999	4013200
2	155.830002	155.830002	2018-02-28	158.139999	155.800003	157.500000	3803500
3	156.550003	156.550003	2018-02-27	159.779999	156.529999	158.460007	4237300
4	158.580002	158.580002	2018-02-26	158.880005	155.509995	155.809998	3610300 '''


df_dividends.head()

'''head call output:
	amount	date	type
0	1.5	2018-02-08	DIVIDEND
1	1.5	2017-11-09	DIVIDEND
2	1.5	2017-08-08	DIVIDEND
3	1.5	2017-05-08	DIVIDEND
4	1.4	2017-02-08	DIVIDEND '''

```
