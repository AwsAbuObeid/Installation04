import time
import numpy as np
from App.tables import PriceVolume, Tech, BTC_Pred, LTC_Pred, XRP_Pred, Stocks
from App import db
from pandas import DataFrame


def getPrices(sampleLength, coin):
    CurrentTime = int(time.time()) - int(time.time()) % 60
    prevTime = (CurrentTime - (sampleLength * 60))
    interval = db.engine.execute(
        'SELECT unix,price' + coin + ',volume' + coin + ' FROM price_volume WHERE unix BETWEEN ? AND ? ORDER BY unix '
                                                        'DESC LIMIT ?', (prevTime, CurrentTime, sampleLength))
    df = DataFrame(interval.fetchall())
    df.columns = interval.keys()
    rows = interval.fetchall()
    if not rows:
        df = DataFrame(columns=interval.keys())
        df.loc[0] = [int(time.time()-((time.time())%60))] +[0] * (len(interval.keys())-1)
    else:
        df = DataFrame(rows)
        df.columns = interval.keys()
    full = Fill(df.to_numpy(), 60,sampleLength)
    return full


def getTech(sampleLength, coin):
    if coin == "BTC":
        CurrentTime = time.time()
        prevTime = (CurrentTime - (sampleLength * 900))
        interval = db.engine. \
            execute('SELECT unix,Mem,TPS,TweetBTC FROM Tech WHERE unix BETWEEN ? AND ? ORDER BY unix DESC',
                    (CurrentTime, prevTime))
        df = DataFrame(interval.fetchall())
        df.columns = interval.keys()
        return Fill(df.to_numpy(), 900,sampleLength)
    else:
        CurrentTime = time.time()
        prevTime = (CurrentTime - (sampleLength * 900))
        interval = db.engine. \
            execute('SELECT unix,Tweet' + coin + ' FROM Tech WHERE unix BETWEEN ? AND ? ORDER BY unix DESC',
                    (CurrentTime, prevTime))

        df = DataFrame(interval.fetchall())
        df.columns = interval.keys()

    return Fill(df.to_numpy(), 900,sampleLength)


def getStocks(sampleLength):
    CurrentTime = time.time()
    prevTime = (CurrentTime - (sampleLength * 900))

    interval = db.engine. \
        execute('SELECT * FROM Stocks WHERE unix BETWEEN ? AND ? ORDER BY unix DESC',
                (CurrentTime, prevTime))
    df = DataFrame(interval.fetchall())
    df.columns = interval.keys()

    return Fill(df.to_numpy(), 900,sampleLength)


def addPrice(unix, Pbtc, Vbtc, Pltc, Vltc, Pxrp, Vxrp):
    unix = int(unix) - int(unix) % 60
    current = PriceVolume(unix=int(unix), priceBTC=Pbtc, volumeBTC=Vbtc
                          , priceLTC=Pltc, volumeLTC=Vltc, priceXRP=Pxrp, volumeXRP=Vxrp)
    db.session.add(current)
    db.session.commit()


def addTech(unix, mem, tps, TweetBTC, TweetLTC, TweetXRP):
    unix = int(unix) - int(unix) % 900
    current = Tech(unix=int(unix), Mem=mem, TPS=tps, TweetBTC=TweetBTC, TweetLTC=TweetLTC, TweetXRP=TweetXRP)
    db.session.add(current)
    db.session.commit()


def addStocks(unix, oil, msci, gld, sp):
    unix = int(unix) - int(unix) % 900
    current = Stocks(unix=unix, oil=oil, msci=msci, gold=gld, sp500=sp)
    db.session.add(current)
    db.session.commit()


def bulkAddPrice(n_p):
    for i in n_p:
        current = PriceVolume(unix=int(i[0]), priceBTC=i[1], volumeBTC=i[2], priceLTC=i[3],
                              volumeLTC=i[4], priceXRP=i[5], volumeXRP=i[6])
        db.session.add(current)
    db.session.commit()


def bulkAddStocks(n_p):
    for i in n_p:
        current = Stocks(unix=int(i[0]), oil=i[1], msci=i[2], gold=i[3], sp500=i[4])
        db.session.add(current)
    db.session.commit()


def bulkAddTech(n_p):
    for i in n_p:
        current = Tech(unix=int(i[0]), Mem=i[1], TPS=i[2], TweetBTC=int(i[3]), TweetLTC=int(i[4]), TweetXRP=int(i[5]))
        db.session.add(current)
    db.session.commit()


def getPred(sampleLength, coin):
    CurrentTime = time.time()
    CurrentTime = int(CurrentTime) - int(CurrentTime) % 900
    prevTime = (CurrentTime - (sampleLength * 900))
    interval = db.engine. \
        execute('SELECT * FROM ' + coin + '__Pred WHERE unix BETWEEN ? AND ? AND unix%900=0 ORDER BY unix DESC',
                (prevTime, CurrentTime))
    rows = interval.fetchall()
    if not rows:
        df = DataFrame(columns=interval.keys())
        df.loc[0] = [int(time.time()-((time.time())%60))] +[0] * (len(interval.keys())-1)
    else:
        df = DataFrame(rows)
        df.columns = interval.keys()
    return df


def add_Pred_all(unix, Pred_30m, Pred_1h, Pred_2h, Pred_4h, Pred_6h, Pred_12h, coin):
    unix = int(unix) - int(unix) % 60
    current = 0
    if coin == "BTC":
        current = BTC_Pred(unix=unix, Pred_30m=Pred_30m, Pred_1h=Pred_1h, Pred_2h=Pred_2h, Pred_4h=Pred_4h
                           , Pred_6h=Pred_6h, Pred_12h=Pred_12h)
    elif coin == "LTC":
        current = LTC_Pred(unix=unix, Pred_30m=Pred_30m, Pred_1h=Pred_1h, Pred_2h=Pred_2h, Pred_4h=Pred_4h
                           , Pred_6h=Pred_6h, Pred_12h=Pred_12h)
    elif coin == "XRP":
        current = XRP_Pred(unix=unix, Pred_30m=Pred_30m, Pred_1h=Pred_1h, Pred_2h=Pred_2h, Pred_4h=Pred_4h
                           , Pred_6h=Pred_6h, Pred_12h=Pred_12h)
    db.session.add(current)
    db.session.commit()


def add_Pred(unix, Pred_30m, Pred_1h, Pred_2h, coin):
    unix = int(unix) - int(unix) % 60
    interval = db.engine.execute('SELECT * FROM ' + coin + '__Pred ORDER BY unix DESC LIMIT 1')
    df = DataFrame(interval.fetchall())
    df.columns = interval.keys()

    if coin == "BTC":
        current = BTC_Pred(unix=unix, Pred_30m=Pred_30m, Pred_1h=Pred_1h, Pred_2h=Pred_2h, Pred_4h=df['Pred_4h'][0]
                           , Pred_6h=df['Pred_6h'][0], Pred_12h=df['Pred_12h'][0])
    elif coin == "LTC":
        current = LTC_Pred(unix=unix, Pred_30m=Pred_30m, Pred_1h=Pred_1h, Pred_2h=Pred_2h, Pred_4h=df['Pred_4h'][0]
                           , Pred_6h=df['Pred_6h'][0], Pred_12h=df['Pred_12h'][0])
    else:
        current = XRP_Pred(unix=unix, Pred_30m=Pred_30m, Pred_1h=Pred_1h, Pred_2h=Pred_2h, Pred_4h=df['Pred_4h'][0]
                           , Pred_6h=df['Pred_6h'][0], Pred_12h=df['Pred_12h'][0])

    db.session.add(current)
    db.session.commit()


def getLatestPreds(coin):
    latest = db.engine.execute('SELECT * FROM ' + coin + '__Pred ORDER BY unix DESC LIMIT 1')
    df = DataFrame(latest.fetchall())
    df.columns = latest.keys()
    n = df.to_numpy()[0]
    return n


def Fill(rows, timeframe,sampleLength):
    new = []
    for i in range(0, len(rows) - 1):
        unix = float(rows[i][0])
        new.append(rows[i])

        if int(rows[i][0]) - int(rows[i + 1][0]) != timeframe:
            N_skips = int((int(rows[i][0]) - int(rows[i + 1][0])) / timeframe)
            tempx = unix
            for n in range(1, N_skips):
                tempx = tempx + timeframe
                row = [tempx]
                for j in range(1, len(rows[0])):
                    row.append(rows[i][j])
                new.append(row)
    for i in range(sampleLength-len(new)):
        new.append(rows[-1])
    return np.array(new)
