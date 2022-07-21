from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from turbo_flask import Turbo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CryptoDB.db'
db = SQLAlchemy(app)
turbo = Turbo(app)

class savedVars:
    btc_tw = 0
    ltc_tw = 0
    xrp_tw = 0


sav = savedVars()

from App import routes
