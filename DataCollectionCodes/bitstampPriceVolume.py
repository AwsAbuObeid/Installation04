import requests
import json

ticker="btcusd"
response = requests.get("https://www.bitstamp.net/api/v2/ticker_hour/"+ticker)
x=json.loads(response.text)
price=x["last"]
volume=x["volume"]

