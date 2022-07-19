import datetime
import requests
import time

D = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y/%m/%d')
url1 = "https://bitinfocharts.com/comparison/btc-tweets.html#3m"

page = requests.get(url1)
y = (page.text[page.text.find('[['):page.text.find(']]') + 2])
ind_btc = y.find(str(D))
ind2_btc = y[ind_btc:].find(']')
Tweets_btc = y[ind_btc + 13:ind_btc + ind2_btc]

