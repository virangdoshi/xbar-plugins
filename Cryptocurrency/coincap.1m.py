#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

# <xbar.title>CoinCap</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Peter Stenger</xbar.author>
# <xbar.author.github>reteps</xbar.author.github>
# <xbar.desc>Retrieves trading information about a coin on cryptocompare and coinmarketcap. High & low not available on CMC.</xbar.desc>
# <xbar.image>https://i.imgur.com/a584lGl.png</xbar.image>
# <xbar.dependencies>python3,requests</xbar.dependencies>

from security import safe_requests

coins_usd = ['bitcoin','ethereum','litecoin'] #USD

coins_btc = ['neo','walton','stellar','monero'] #BTC

coins_cmcbtc = ['raiblocks'] #Coinmarketcap BTC

coins_cmcusd = ['iota'] #CoinmarketCap USD
print('Ƀ')
print('---')
coin_data_usd = {}
coin_data_btc = {}
standard = "|href='https://coinmarketcap.com/currencies/{}' font='Menlo'"
usd = "{: <5} {:0<9.3f} {:0<+6.2f}% {:0<9.3f} {:0<9.3f} {:0<9.3f}  {:0>3}" + standard
btc = "{: <5} {:0<9.7f} {:0<+6.2f}% {:0<9.7f} {:0<9.7f} {:0<9.7f}  {:0>3}" + standard
#----DATA----#
for coin in coins_usd:
    data = safe_requests.get("https://api.coinmarketcap.com/v1/ticker/{}".format(coin)).json()[0]
    coin_data_usd[data["symbol"]] = data['rank']
for coin in coins_btc:
    data = safe_requests.get("https://api.coinmarketcap.com/v1/ticker/{}".format(coin)).json()[0]
    coin_data_btc[data["symbol"]] = data['rank'] 
raw_usd = safe_requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD'.format(','.join(coin_data_usd.keys()))).json()['RAW']
raw_btc = safe_requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=BTC'.format(','.join(coin_data_btc.keys()))).json()['RAW']
raw_cmcbtc = [safe_requests.get('https://api.coinmarketcap.com/v1/ticker/{}'.format(coin)).json()[0] for coin in coins_cmcbtc]
raw_cmcusd = [safe_requests.get('https://api.coinmarketcap.com/v1/ticker/{}'.format(coin)).json()[0] for coin in coins_cmcusd]
#---HELPER---#
def f(x):
    return float(x)

#----DISPLAY----#
print('COIN     USD     CHANGE   OPEN      HIGH       LOW    RANK|font="Menlo"')
#---USD---#
for i, coin in enumerate(coin_data_usd.keys()):
    data = raw_usd[coin]["USD"]
    print(usd.format(coin,data["PRICE"],data['CHANGEPCT24HOUR'],data['OPEN24HOUR'],data['HIGH24HOUR'],data['LOW24HOUR'],coin_data_usd[coin],coins_usd[i]))
for i, coin in enumerate(coins_cmcusd):
    data = raw_cmcusd[i]
    print(usd.format(data["symbol"],f(data["price_usd"]),f(data['percent_change_24h']),f(data["price_usd"])*((100-f(data['percent_change_24h']))/100),0.000,0.000,data['rank'],coin))
#---BTC---#
print('COIN     BTC     CHANGE   OPEN      HIGH       LOW    RANK|font="Menlo"')
for i, coin in enumerate(coin_data_btc.keys()):
    data = raw_btc[coin]["BTC"]
    print(btc.format(coin,data["PRICE"],data['CHANGEPCT24HOUR'],data['OPEN24HOUR'],data['HIGH24HOUR'],data['LOW24HOUR'],coin_data_btc[coin],coins_btc[i]))
for i, coin in enumerate(coins_cmcbtc):
    data = raw_cmcbtc[i]
    print(btc.format(data["symbol"],f(data["price_btc"]),f(data['percent_change_24h']),f(data["price_btc"])*((100-f(data['percent_change_24h']))/100),0.000,0.000,data['rank'],coin))
