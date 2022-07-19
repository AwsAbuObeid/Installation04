from App import db


class PriceVolume(db.Model):
    unix = db.Column(db.Integer, nullable=False, primary_key=True)
    priceBTC = db.Column(db.Float, nullable=False)
    volumeBTC = db.Column(db.Float, nullable=False)
    priceLTC = db.Column(db.Float, nullable=False)
    volumeLTC = db.Column(db.Float, nullable=False)
    priceXRP = db.Column(db.Float, nullable=False)
    volumeXRP = db.Column(db.Float, nullable=False)


class Tech(db.Model):
    unix = db.Column(db.Integer, nullable=False, primary_key=True)
    Mem = db.Column(db.Float, nullable=False)
    TPS = db.Column(db.Float, nullable=False)
    TweetBTC = db.Column(db.Integer, nullable=False)
    TweetLTC = db.Column(db.Integer, nullable=False)
    TweetXRP = db.Column(db.Integer, nullable=False)


class Stocks(db.Model):
    unix = db.Column(db.Integer, nullable=False, primary_key=True)
    oil = db.Column(db.Float, nullable=False)
    msci = db.Column(db.Float, nullable=False)
    gold = db.Column(db.Float, nullable=False)
    sp500 = db.Column(db.Float, nullable=False)


class BTC_Pred(db.Model):
    unix = db.Column(db.Integer, nullable=False, primary_key=True)
    Pred_30m = db.Column(db.Boolean, nullable=False)
    Pred_1h = db.Column(db.Boolean, nullable=False)
    Pred_2h = db.Column(db.Boolean, nullable=False)
    Pred_4h = db.Column(db.Boolean, nullable=False)
    Pred_6h = db.Column(db.Boolean, nullable=False)
    Pred_12h = db.Column(db.Boolean, nullable=False)


class LTC_Pred(db.Model):
    unix = db.Column(db.Integer, nullable=False, primary_key=True)
    Pred_30m = db.Column(db.Boolean, nullable=False)
    Pred_1h = db.Column(db.Boolean, nullable=False)
    Pred_2h = db.Column(db.Boolean, nullable=False)
    Pred_4h = db.Column(db.Boolean, nullable=False)
    Pred_6h = db.Column(db.Boolean, nullable=False)
    Pred_12h = db.Column(db.Boolean, nullable=False)


class XRP_Pred(db.Model):
    unix = db.Column(db.Integer, nullable=False, primary_key=True)
    Pred_30m = db.Column(db.Boolean, nullable=False)
    Pred_1h = db.Column(db.Boolean, nullable=False)
    Pred_2h = db.Column(db.Boolean, nullable=False)
    Pred_4h = db.Column(db.Boolean, nullable=False)
    Pred_6h = db.Column(db.Boolean, nullable=False)
    Pred_12h = db.Column(db.Boolean, nullable=False)
