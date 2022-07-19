import time
from App.NN.Model import Model
from data.CryptoDao import getPrices, add_Pred, add_Pred_all

dir = r"C:\Users\awsab\IdeaProjects\crypto\App"

btc_30min = Model(dir + r"\NN\btc_30min_pkg")
btc_1h = Model(dir + r"\NN\btc_1h_pkg")
btc_2h = Model(dir + r"\NN\btc_2h_pkg")
btc_4h = Model(dir + r"\NN\btc_4h_pkg")
btc_6h = Model(dir + r"\NN\btc_6h_pkg")
btc_12h = Model(dir + r"\NN\btc_12h_pkg")

ltc_30min = Model(dir + r"\NN\ltc_30min_pkg")
ltc_1h = Model(dir + r"\NN\ltc_1h_pkg")
ltc_2h = Model(dir + r"\NN\ltc_2h_pkg")
ltc_4h = Model(dir + r"\NN\ltc_4h_pkg")
ltc_6h = Model(dir + r"\NN\ltc_6h_pkg")
ltc_12h = Model(dir + r"\NN\ltc_12h_pkg")

xrp_30min = Model(dir + r"\NN\xrp_30min_pkg")
xrp_1h = Model(dir + r"\NN\xrp_1h_pkg")
xrp_2h = Model(dir + r"\NN\xrp_2h_pkg")
xrp_4h = Model(dir + r"\NN\xrp_4h_pkg")
xrp_6h = Model(dir + r"\NN\xrp_6h_pkg")
xrp_12h = Model(dir + r"\NN\xrp_12h_pkg")

def updateOneMinModels():
    if int(time.time()) % 900 == 0:
        return
    print("___Updating BTC minute models___")
    interval = getPrices(btc_30min.sampleLength, btc_30min.coin)
    p30 = btc_30min.predict(interval)

    interval = getPrices(btc_1h.sampleLength, btc_1h.coin)
    p1 = btc_1h.predict(interval)

    interval = getPrices(btc_2h.sampleLength, btc_2h.coin)
    p2 = btc_2h.predict(interval)
    add_Pred(int(time.time()), p30, p1, p2, "BTC")

    print("___Updating LTC minute models___")
    interval = getPrices(ltc_30min.sampleLength, ltc_30min.coin)
    p30 = ltc_30min.predict(interval)

    interval = getPrices(ltc_1h.sampleLength, ltc_1h.coin)
    p1 = ltc_1h.predict(interval)

    interval = getPrices(ltc_2h.sampleLength, ltc_2h.coin)
    p2 = ltc_2h.predict(interval)
    add_Pred(int(time.time()), p30, p1, p2, "LTC")

    print("___Updating XRP minute models___")
    interval = getPrices(xrp_30min.sampleLength, xrp_30min.coin)
    p30 = xrp_30min.predict(interval)

    interval = getPrices(xrp_1h.sampleLength, xrp_1h.coin)
    p1 = xrp_1h.predict(interval)

    interval = getPrices(xrp_2h.sampleLength, xrp_2h.coin)
    p2 = xrp_2h.predict(interval)
    add_Pred(int(time.time()), p30, p1, p2, "XRP")



def update15MinModels():
    print("___Updating BTC 15 minute models___")
    interval = getPrices(btc_30min.sampleLength, btc_30min.coin)
    p30 = btc_30min.predict(interval)

    interval = getPrices(btc_1h.sampleLength, btc_1h.coin)
    p1 = btc_1h.predict(interval)

    interval = getPrices(btc_2h.sampleLength, btc_2h.coin)
    p2 = btc_2h.predict(interval)

    interval = getPrices(btc_4h.sampleLength, btc_4h.coin)
    p4 = btc_4h.predict(interval)

    interval = getPrices(btc_6h.sampleLength, btc_6h.coin)
    p6 = btc_6h.predict(interval)

    interval = getPrices(btc_12h.sampleLength, btc_12h.coin)
    p12 = btc_12h.predict(interval)
    add_Pred_all(int(time.time()), p30, p1, p2, p4, p6, p12, "BTC")

    print("___Updating LTC 15 minute models___")

    interval = getPrices(ltc_30min.sampleLength, ltc_30min.coin)
    p30 = ltc_30min.predict(interval)

    interval = getPrices(ltc_1h.sampleLength, ltc_1h.coin)
    p1 = ltc_1h.predict(interval)

    interval = getPrices(ltc_2h.sampleLength, ltc_2h.coin)
    p2 = ltc_2h.predict(interval)

    interval = getPrices(ltc_4h.sampleLength, ltc_4h.coin)
    p4 = ltc_4h.predict(interval)

    interval = getPrices(ltc_6h.sampleLength, ltc_6h.coin)
    p6 = ltc_6h.predict(interval)

    interval = getPrices(ltc_12h.sampleLength, ltc_12h.coin)
    p12 = ltc_12h.predict(interval)
    add_Pred_all(int(time.time()), p30, p1, p2, p4, p6, p12, "LTC")

    print("___Updating XRP 15 minute models___")

    interval = getPrices(xrp_30min.sampleLength, xrp_30min.coin)
    p30 = xrp_30min.predict(interval)

    interval = getPrices(xrp_1h.sampleLength, xrp_1h.coin)
    p1 = xrp_1h.predict(interval)

    interval = getPrices(xrp_2h.sampleLength, xrp_2h.coin)
    p2 = xrp_2h.predict(interval)

    interval = getPrices(xrp_4h.sampleLength, xrp_4h.coin)
    p4 = xrp_4h.predict(interval)

    interval = getPrices(xrp_6h.sampleLength, xrp_6h.coin)
    p6 = xrp_6h.predict(interval)

    interval = getPrices(xrp_12h.sampleLength, xrp_12h.coin)
    p12 = xrp_12h.predict(interval)

    add_Pred_all(int(time.time()), p30, p1, p2, p4, p6, p12, "XRP")
