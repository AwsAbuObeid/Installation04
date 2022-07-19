import yfinance as yf

T_oil = yf.Ticker("CL=F")
T_msci = yf.Ticker("MSCI")
T_gold = yf.Ticker("GC=F")
T_sp500 = yf.Ticker("^GSPC")

I_oil = T_oil.info
I_msci = T_msci.info
I_gold = T_gold.info
I_sp500 = T_sp500.info

price_oil = I_oil["ask"]
price_msci = I_msci["currentPrice"]
price_gold = I_gold["ask"]
price_sp500 = I_sp500["ask"]
