import os
from binance.client import Client
import pandas as pd
import talib
import time
import requests
from binance.um_futures import UMFutures
from datetime import datetime, timedelta
import logging
from binance.error import ClientError
API_KEY = ''
SECRET_KEY = ''
# BASE_URL = 'https://testnet.binancefuture.com'
BASE_URL = 'https://fapi.binance.com'
um_futures_client = UMFutures(key=API_KEY, secret=SECRET_KEY, base_url=BASE_URL)
# 設置你的API密鑰
api_key = os.environ.get('')
api_secret = os.environ.get('')
# 初始化Binance客戶端
client = Client(api_key, api_secret)


def lineNotifyMessage(token, msg):

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code
# 下載歷史K線數據
def klines_data(client, symbol, interval, filepath, crypto_data_ALL):
    # 獲取當前日期和時間
    current_time = datetime.now().date()
    # 計算前500天的日期
    delta = timedelta(days=100)
    past_time = current_time - delta
    klines = client.get_historical_klines(symbol, interval, str(past_time), "14 Sep 2030")
    data = pd.DataFrame(klines,
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.to_csv(crypto_data_ALL, index=False, encoding='big5')
    df = pd.read_csv(crypto_data_ALL, encoding='big5')
    return df
#下載2筆資料
def get_klines_data(symbol, interval, limit):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
RR = []
def RSI(symbol, filepath, interval, crypto_data_ALL):
    if not os.path.isfile(crypto_data_ALL):
        da = klines_data(client, symbol, interval, filepath, crypto_data_ALL)
    else:
        df_2 = get_klines_data(symbol, interval, 2)
        # df_2 = df_2.drop(1, axis=0)
        df = pd.read_csv(crypto_data_ALL, encoding='big5')
        df = df.drop(len(df) - 1, axis=0)

        combined_df = pd.concat([df, df_2], ignore_index=True)
        combined_df.to_csv(crypto_data_ALL, index=False, encoding='big5')

        da = pd.read_csv(crypto_data_ALL, encoding='big5')
    # da = data_t(i, filepath, interval)
    RSI = talib.RSI(da.close)
    data = pd.DataFrame(RSI, columns=['RSI'])
    RSI_data = data.loc[len(data) - 2, 'RSI']
    if RSI_data >= 65:
        RR.append(i + ':SELL '+interval)
    if RSI_data <= 35:
        RR.append(i + ':PUY '+interval)
    return RR
# token = 'GgtfHs2Vb50pNx6AAnOlF9eQIErAIEQY839bPfkwzEG' 個人
token = 'MxCPNCqHrd58sp2XZSvWFromq9v76Tmi7sWkCKCycvC'
message = ''
# 設置所需的市場和時間間隔
# "1m", "5m",'15m', '30m', "1h", '2h', "4h", "12h", "1d",
symbol = ["FLOKIUSDT", "LUNCUSDT", "PEPEUSDT", "SHIBUSDT", "XECUSDT", "1INCHUSDT", "AAVEUSDT", "ACHUSDT", "ADAUSDT",
"AGIXUSDT", "AGLDUSDT", "ALGOUSDT", "ALICEUSDT", "ALPHAUSDT", "AMBUSDT", "ANKRUSDT", "ANTUSDT", "APEUSDT",
"API3USDT", "APTUSDT", "ARBUSDT", "ARKMUSDT", "ARPAUSDT", "ARUSDT", "ASTRUSDT", "ATAUSDT", "ATOMUSDT",
"AUDIOUSDT", "AVAXUSDT","AXSUSDT", "BAKEUSDT", "BALUSDT", "BANDUSDT", "BATUSDT", "BCHUSDT", "BELUSDT", "BLZUSDT",
"BNBUSDT", "BNTUSDT", "BNXUSDT", "BTCUSDT", "C98USDT", "CELOUSDT", "CELRUSDT", "CFXUSDT", "CHRUSDT",
"CHZUSDT", "CKBUSDT", "COMBOUSDT", "COMPUSDT", "COTIUSDT", "CRVUSDT", "CTKUSDT", "CTSIUSDT", "CVXUSDT", "CYBERUSDT",
          "DARUSDT", "DASHUSDT", "DENTUSDT", "DGBUSDT", "DODOUSDT", "DOGEUSDT", "DOTUSDT", "DUSKUSDT", "DYDXUSDT",
          "EDUUSDT", "EGLDUSDT", "ENJUSDT", "ENSUSDT", "EOSUSDT", "ETCUSDT", "ETHBTC", "ETHUSDT", "FETUSDT", "FILUSDT",
          "FLMUSDT", "FLOWUSDT", "FTMUSDT", "FXSUSDT", "GALAUSDT", "GALUSDT", "GMTUSDT", "GMXUSDT", "GRTUSDT","GTCUSDT", "HBARUSDT", "HFTUSDT", "HIGHUSDT", "HOOKUSDT", "HOTUSDT", "ICPUSDT", "ICXUSDT", "IDEXUSDT", "IDUSDT",
"IMXUSDT", "INJUSDT", "IOSTUSDT", "IOTAUSDT", "IOTXUSDT", "JASMYUSDT", "JOEUSDT", "KAVAUSDT", "KEYUSDT", "KNCUSDT",
"KSMUSDT", "LDOUSDT", "LEVERUSDT", "LINAUSDT", "LINKUSDT", "LITUSDT", "LPTUSDT", "LQTYUSDT", "LRCUSDT", "LTCUSDT","LUNAUSDT", "MAGICUSDT", "MANAUSDT", "MASKUSDT", "MATICUSDT", "MAVUSDT", "MDTUSDT", "MINAUSDT", "MKRUSDT", "MTLUSDT",
"NEARUSDT", "NEOUSDT", "NKNUSDT", "NMRUSDT", "OCEANUSDT", "OGNUSDT", "OMGUSDT", "ONEUSDT", "ONTUSDT", "OPUSDT",
"OXTUSDT", "PENDLEUSDT", "PEOPLEUSDT", "PERPUSDT", "PHBUSDT", "QNTUSDT", "QTUMUSDT", "RADUSDT", "RDNTUSDT", "REEFUSDT","RENUSDT", "RLCUSDT", "RNDRUSDT", "ROSEUSDT", "RSRUSDT", "RUNEUSDT", "RVNUSDT", "SANDUSDT", "SEIUSDT", "SFPUSDT",
"SKLUSDT", "SNXUSDT", "SOLUSDT", "SPELLUSDT", "SSVUSDT", "STGUSDT", "STMXUSDT", "STORJUSDT", "STXUSDT", "SUIUSDT",
"SUSHIUSDT", "SXPUSDT", "THETAUSDT", "TLMUSDT", "TOMOUSDT", "TRBUSDT", "TRUUSDT", "TRXUSDT", "TUSDT", "UMAUSDT",
"UNFIUSDT","UNIUSDT", "USDCUSDT", "VETUSDT", "WAVESUSDT", "WLDUSDT", "WOOUSDT", "XEMUSDT", "XLMUSDT", "XMRUSDT", "XRPUSDT",
"XTZUSDT", "XVGUSDT", "XVSUSDT", "YFIUSDT", "YGGUSDT", "ZECUSDT", "ZENUSDT", "ZILUSDT", "ZRXUSDT"]
interval = '1h'  # 1日K線

crypto_data_ALL = 'D:/pycharm/crypto_data_ALL/'
while True:
    # 獲取當前時間的分鐘和秒數
    current_time = time.localtime()
    # print('current_time:',current_time)
    minutes = current_time.tm_min
    #print('minutes:', minutes)
    seconds = current_time.tm_sec
    # print('seconds:', seconds)
    hour = current_time.tm_hour
    # 4h
    # if hour % 4 == 0 and minutes == 0 and seconds == 0:
    # 15m
    # if minutes % 15 == 0 and seconds == 0:
    if minutes == 0 and seconds == 0:

        # 在這裡執行您希望在整點時執行的代碼
        print("整點操作執行中...")
        while True:
            current_timestamp = time.time()
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_timestamp))
            ord_time = current_timestamp
            print('現在的時間是：', current_time)
            for i in symbol:
                filepath = i + '.csv'
                crypto_data_ALL = crypto_data_ALL + filepath
                RSI_data = RSI(i, filepath, interval, crypto_data_ALL)
                crypto_data_ALL = 'D:/pycharm/crypto_data_ALL/'
                # time.sleep(5)
            # RSI_data = RSI(symbol, interval, 1500)

            ra = 0
            for i in RSI_data:
                if ra == 0:
                    message = 'RSI:\n'
                    message = message + '{}\n'.format(i)
                    ra = ra + 1
                else:
                    message = message + '{}\n'.format(i)
            print(message)
            lineNotifyMessage(token, message)
            current_timestamp = time.time()
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_timestamp))
            current_timestamp = current_timestamp - ord_time
            print('現在的時間是：', current_time)
            if current_timestamp > 60:
                print('計算時間', current_timestamp / 60)
            else:
                print('計算時間', current_timestamp)
            current_timestamp = 0
            break
        # 等待一分鐘，避免重複執行
        time.sleep(60)
    else:
        RR = []
        # 如果不是整點，等待1秒後再檢查
        time.sleep(1)