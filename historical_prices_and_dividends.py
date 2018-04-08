import requests
import datetime
import json
import pandas as pd


def _convert_epoch_to_datetime(epoch_seconds):
    epoch = datetime.datetime(1970, 1, 1)
    dt = epoch + datetime.timedelta(seconds=epoch_seconds)
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def _convert_datetime_to_epoch(start):
    dt = pd.to_datetime(start)
    epoch = datetime.datetime(1970, 1, 1)

    return int((dt - epoch).total_seconds())


# Collect historical prices from yahoo finance for the given ticker for the time period of start_date to end_date.
#
# ticker(string) - stock ticker in caps, ex: AAPL, IBM, IVV
# start_date(datetime) - earliest date to collect price for the given ticker
# end_date(datetime) - latest date to collect price for the given ticker
def get_prices(ticker=None, start='01/01/1970', end=datetime.datetime.now()):
    # convert datetimes to epoch
    dstart_secs = _convert_datetime_to_epoch(start)
    dend_secs = _convert_datetime_to_epoch(end)

    # set url for yahoo finance with filled in parameters
    url = "https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d".format(ticker, dstart_secs, dend_secs)
        
    response = requests.get(url).content

    # find the json object in the response, format it, and load it
    index_s = response.find("HistoricalPriceStore")
    index_e = response.find("isPending", index_s)

    response = response[index_s:index_e]
    json_string = response[22:len(response) - 2] + "}"

    mm = json.loads(json_string)
    df = pd.DataFrame(mm['prices'])
    df["date"] = df["date"].apply(lambda x: _convert_epoch_to_datetime(x))
    df.set_index('date', inplace=True)
    df = df.sort_index()
    df = df[['close', 'adjclose', 'volume']]
    df = df.dropna()
    return df


# Collect historical dividends from yahoo finance for the given ticker for the time period of start_date to end_date.
#
# ticker(string) - stock ticker in caps, ex: AAPL, IBM, IVV
# start_date(datetime) - earliest date to collect price for the given ticker
# end_date(datetime) - latest date to collect price for the given ticker
def get_divs(ticker=None, start='01/01/1970', end=datetime.datetime.now()):

    # convert datetimes to epoch
    dstart_secs = _convert_datetime_to_epoch(start)
    dend_secs = _convert_datetime_to_epoch(end)

    # set url for yahoo finance with filled in parameters
    url = "https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d".format(ticker, dstart_secs, dend_secs)
        

    response = requests.get(url).content

    # find the json object in the response, format it, and load it
    index_s = response.find("HistoricalPriceStore")
    index_e = response.find("isPending", index_s)

    response = response[index_s:index_e]
    json_string = response[22:len(response) - 2] + "}"

    mm = json.loads(json_string)
    dividends = []
    for row in mm["prices"]:
        if "type" in row:
            dividends.append(row)
	df_dividends = pd.DataFrame.from_dict(dividends)
	
    
    
    df_dividends["date"] = df_dividends["date"].apply(lambda x: _convert_epoch_to_datetime(x))
    df_dividends.set_index('date', inplace=True)
    df_dividends = df_dividends[['amount']]
    df_dividends = df_dividends.sort_index()
    
    return df_dividends
	
def get_yield(sym, start='01/01/1970', end=datetime.datetime.now()):

    dfdiv = get_divs(sym, start='01/01/1970', end=datetime.datetime.now())
    df = get_prices(sym, start='01/01/1970', end=datetime.datetime.now())['close']

    rolldfdiv = dfdiv.rolling(len(dfdiv.loc[str(datetime.datetime.now().year-1)])).sum()

    result = pd.concat([df, rolldfdiv], axis=1, join_axes=[df.index]).fillna(method='ffill')

    return result['amount']/result['close']*100	
