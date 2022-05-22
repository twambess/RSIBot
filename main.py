import json
import numpy
import pprint
import talib
import websocket
from binance.client import Client
from binance.enums import *

SOCKET ="wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD=14
RSI_OVERBOUGHT=70
RSI_OVERSOLD=30
TRADE_SYMBOL='ETHUSDT'
TRADE_QUANTITY = 0.05

API_KEY ="r0SG9mA4bSmwCKXmTSzJtJIFyNTRj9TTzMwXQMIOzqyFK2tSqsRMgUkZP2zh5xTB"
API_SECRET="RBwylXmsjOy6rrgDSM1dinJdhfcoBBT3nEeHnNXTNyrHWH2EibNvuRdiJKtGHBbo"

#client = Client(API_KEY, API_SECRET, tld='ru')

closes=[]
in_position = False


def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws,message):
    global closes
    print('received message')
    json_message=json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed=candle['x']
    close=candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi=talib.RSI(np_closes,RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi=rsi[-1]
            print("the current rsi is {}".format(last_rsi))
            if last_rsi>RSI_OVERBOUGHT:
                if in_position:
                    print("It is overbought! Sell! Sell! Sell!")
                    #put binance sell order logic here
                else:
                    print("We dont own any, nothing to do")

            if last_rsi>RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do")
                else:
                    print("Buy! Buy! Buy!")
                    #put binance buy order logic here


ws=websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()


