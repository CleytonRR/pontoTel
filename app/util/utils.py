from alpha_vantage.async_support.timeseries import TimeSeries
import requests


KEY='KRDPNX5BS3VEZYW2'
ts = TimeSeries(key=KEY)

async def get_price(nome):
    data, meta_data = await ts.get_intraday(nome)
    for i in data:
        price = data[i]['4. close']
        break
    return price

def valid_name(nome):
    dados = requests.get(
        'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}'
            .format(nome, KEY))
    if dados.json()['bestMatches'] == []:
        return False
    return True