from datetime import datetime

from flask import render_template, redirect
from App import app
from data.CryptoDao import getPred, getLatestPreds
import time
import threading


@app.route('/', methods=["GET", "POST"])
def Welcome():
    return redirect("/Bitcoin")


@app.route('/Litecoin')
def LiteCoin():
    return render_template("index.html", coin='Litecoin', ticker=359)


@app.route('/Ripple')
def Ripple():
    return render_template("index.html", coin='Ripple', ticker=619)


@app.route('/Bitcoin')
def Bitcoin():
    return render_template("index.html", coin='Bitcoin', ticker=859)


@app.route('/pred')
def Pred():
    BTC = getLatestPreds("BTC")
    LTC = getLatestPreds("LTC")
    XRP = getLatestPreds("XRP")
    dict = {
        "BTC":BTC,
        "LTC":LTC,
        "XRP": XRP
    }
    return dict


from data.CryptoDao import getLatestPreds
from App import turbo


@app.context_processor
def inject_load():
    btc = getLatestPreds("BTC")[1:].tolist()
    ltc = getLatestPreds("LTC")[1:].tolist()
    xrp = getLatestPreds("XRP")[1:].tolist()

    btc_preds = getPred(12, "BTC")
    btc_M = btc_preds.loc[:, btc_preds.columns != 'unix'].to_numpy()
    unix = btc_preds['unix'].to_numpy()
    time = []
    for i in range(len(unix)):
        time.append(datetime.utcfromtimestamp(int(unix[i]) + 10800).strftime('%H:%M'))

    ltc_preds = getPred(12, "LTC")
    ltc_M = ltc_preds.loc[:, ltc_preds.columns != 'unix'].to_numpy()

    xrp_preds = getPred(12, "XRP")
    xrp_M = xrp_preds.loc[:, xrp_preds.columns != 'unix'].to_numpy()

    return {'btc': btc
        , 'xrp': xrp
        , 'ltc': ltc
        , 'btc_M': btc_M
        , 'ltc_M': ltc_M
        , 'xrp_M': xrp_M
        , 'time': time
        , 'lenBTC': len(btc_M)
        , 'lenLTC': len(ltc_M)
        , 'lenXRP': len(xrp_M)
            }


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


def update_load():
    with app.app_context():
        while True:
            turbo.push(turbo.replace(render_template('preds_btc.html'), 'load'))
            turbo.push(turbo.replace(render_template('preds_ltc.html'), 'load2'))
            turbo.push(turbo.replace(render_template('preds_xrp.html'), 'load3'))
            turbo.push(turbo.replace(render_template('table_btc.html'), 'load4'))
            turbo.push(turbo.replace(render_template('table_ltc.html'), 'load5'))
            turbo.push(turbo.replace(render_template('table_xrp.html'), 'load6'))
            time.sleep(5)
