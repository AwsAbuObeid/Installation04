from data.CryptoDao import addPrice, addTech, addStocks
import datetime
import requests
import yfinance as yf
from websocket import create_connection
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
from App import sav


def UpdatePriceVolume():
    unix = time.time()
    while True:
        a, b, c, d, e, f = getPriceVolume()
        if a == -1 and (time.time() - unix) < 30:
            continue
        if a != -1:
            addPrice(unix, a, b, c, d, e, f)
            return
        print("Couldnt get prices at :", unix)
        return


def UpdateTech():
    unix = time.time()
    while True:
        mem = getMem()
        tps = getTPS()
        t1, t2, t3 = getTweetCount()
        if (mem == -1 or tps == -1 or t1 == -1) and (time.time() - unix) < 600:
            continue
        if mem != -1 or tps != -1 or t1 != -1:
            mem = mem if mem != -1 else 0
            tps = tps if tps != -1 else 0
            t1 = t1 if t1 != -1 else 0
            t2 = t2 if t2 != -1 else 0
            t3 = t3 if t3 != -1 else 0
            addTech(unix, mem, tps, t1, t2, t3)
            return
        print("Couldnt get Tech at :", unix)
        return


def UpdateStocks():
    unix = time.time()
    while True:
        o, m, g, s = getStocks()
        if o == -1 and (time.time() - unix) < 600:
            continue
        if o != -1:
            addStocks(unix, o, m, g, s)
            return
        print("Couldnt get stocks at :", unix)
        return


def getPriceVolume():
    try:
        response = requests.get("https://www.bitstamp.net/api/v2/ticker_hour/btcusd/")
        x = json.loads(response.text)
        btcP = x["last"]
        btcV = x["volume"]
        response = requests.get("https://www.bitstamp.net/api/v2/ticker_hour/ltcusd/")
        x = json.loads(response.text)
        ltcP = x["last"]
        ltcV = x["volume"]
        response = requests.get("https://www.bitstamp.net/api/v2/ticker_hour/xrpusd/")
        x = json.loads(response.text)
        xrpP = x["last"]
        xrpV = x["volume"]

        return float(btcP), float(btcV), float(ltcP), float(ltcV), float(xrpP), float(xrpV)
    except:
        return -1, -1, -1, -1, -1, -1


def getTweetCount():
    try:
        D = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y/%m/%d')

        url1 = "https://bitinfocharts.com/comparison/btc-tweets.html#3m"
        url2 = "https://bitinfocharts.com/comparison/ltc-tweets.html#3m"
        url3 = "https://bitinfocharts.com/comparison/xrp-tweets.html#3m"

        page = requests.get(url1)
        y = (page.text[page.text.find('[['):page.text.find(']]') + 2])
        ind_btc = y.find(str(D))
        ind2_btc = y[ind_btc:].find(']')
        NT_btc = y[ind_btc + 13:ind_btc + ind2_btc]

        page = requests.get(url2)
        y = (page.text[page.text.find('[['):page.text.find(']]') + 2])
        ind_ltc = y.find(str(D))
        ind2_ltc = y[ind_ltc:].find(']')
        NT_ltc = y[ind_ltc + 13:ind_ltc + ind2_ltc]

        page = requests.get(url3)
        y = (page.text[page.text.find('[['):page.text.find(']]') + 2])
        ind_xrp = y.find(str(D))
        ind2_xrp = y[ind_xrp:].find(']')
        NT_xrp = y[ind_xrp + 13:ind_xrp + ind2_xrp]
        if len(NT_btc) > 10 or len(NT_ltc) > 10 or len(NT_xrp) > 10:
            return 0, 0, 0

        btc = int(NT_btc) - sav.btc_tw
        ltc = int(NT_ltc) - sav.ltc_tw
        xrp = int(NT_xrp) + sav.xrp_tw

        sav.btc_tw = int(NT_btc)
        sav.ltc_tw = int(NT_ltc)
        sav.xrp_tw = int(NT_xrp)
        return btc, ltc, xrp
    except:
        return -1, -1, -1


def getStocks():
    try:
        T_oil = yf.Ticker("CL=F")
        T_msci = yf.Ticker("MSCI")
        T_gold = yf.Ticker("GC=F")
        T_sp500 = yf.Ticker("^GSPC")

        I_oil = T_oil.info
        I_msci = T_msci.info
        I_gold = T_gold.info
        I_sp500 = T_sp500.info

        p_oil = I_oil["ask"]
        p_msci = I_msci["currentPrice"]
        p_gold = I_gold["ask"]
        P_sp500 = I_sp500["ask"]
        return float(p_oil), float(p_msci), float(p_gold), float(P_sp500)
    except:
        return -1, -1, -1, -1


def getMem():
    try:
        t = int(time.time())
        ws = create_connection("wss://bitcoin.clarkmoody.com/dashboard/ws")
        ws.send("""{"op":"c","ch":"","pl":{"c":"4de43be4236035c5","s":"9f6e08f07c263998"}}""")
        ws.send("""{"op":"sub","ch":"mod"}""")
        ws.send("""{"op":"sub","ch":"sta"}""")
        ws.send("""{"op":"sub","ch":"sys"}""")
        ws.send("""{"op":"sub","ch":"upd"}""")

        ws.recv()
        ws.recv()
        ws.recv()
        ws.recv()
        x = json.loads(ws.recv())

        mem = x["pl"]["mt"]
        return float(mem)
    except:
        return -1


def getTPS():
    try:
        path = "D:\program files\chromedriver.exe"
        service = Service(path)
        service.creationflags = CREATE_NO_WINDOW

        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome('D:\program files\chromedriver.exe', options=options)

        driver.get("https://statoshi.info/?orgId=1")
        sleep(3)
        content = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        index = content.find("graph-legend-value current")
        index = content.find("graph-legend-value current", index + 28)
        TPS = content[index + 28:index + 32]
        driver.quit()
        return float(TPS)
    except:
        return -1
