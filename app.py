import pandas as pd
import engine

app = engine.engine()

AMOUNT = 20
HELPER1 = 0
HELPER2 = 0
TRADING = False
MULTIPLIER = 5
while 1:
    try:
        if not TRADING:
            price1 = app.get_AskPrice("BNBUSD_PERP",AMOUNT*MULTIPLIER/2)
            price2 = app.get_BidPrice("BNBUSD_210625",AMOUNT*MULTIPLIER/2) #210625
            print("AMOUNT ",AMOUNT)
            if price1 < price2*(1-0.0008):
                HELPER1 = (AMOUNT * MULTIPLIER/ 2) / price1 * (1-0.0004)
                HELPER2 = (AMOUNT * MULTIPLIER/ 2) * price2 * (1-0.0004)
                TRADING = True
        else:
            price1 = app.get_BidPrice("BNBUSD_PERP",AMOUNT*MULTIPLIER/2)
            price2 = app.get_AskPrice("BNBUSD_210625",AMOUNT*MULTIPLIER/2) #210625
            profit1 = HELPER1 * price1 * (1-0.0004)
            profit2 = HELPER2 / price2 * (1-0.0004)
            profit = round((profit1 + profit2) - AMOUNT * MULTIPLIER,2)
            print("Potential ",round(profit + AMOUNT,2)," profit ",profit," AMOUNT ",AMOUNT," profit1 ",round(profit1-AMOUNT/2*MULTIPLIER,2)," profit2 ",round(profit2-AMOUNT/2*MULTIPLIER,2))
            if profit1 - AMOUNT/2*MULTIPLIER <= -AMOUNT/2 or profit2 - AMOUNT/2*MULTIPLIER <= -AMOUNT/2:
                app.additlog("Trades.csv",[price1,price2,HELPER1,HELPER2,profit1,profit2,AMOUNT])
                AMOUNT = round(profit + AMOUNT,2)
                HELPER1 = 0
                HELPER2 = 0
                TRADING = False
            if profit + AMOUNT > AMOUNT+0.1:
                app.additlog("Trades.csv",[price1,price2,HELPER1,HELPER2,profit1,profit2,AMOUNT])
                AMOUNT = round(profit + AMOUNT,2)
                HELPER1 = 0
                HELPER2 = 0
                TRADING = False
    except:
        print("There was an error")