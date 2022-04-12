# @file market.py
# @author Kuan-Di Jiang
# @brief Connect web API and data pre-processing 

from numpy import histogram, shares_memory
import pandas as pd
# from pandas.io.formats import style
import requests
import numpy as np
from datetime import datetime, time
from talib import abstract
import matplotlib.pyplot as plt
#import mpl_finance as mpf  #dismiss in 2020
import mplfinance as mpf    #upgrade mode in 2020
# # DataFrame Setting
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',100)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# # Global Variables Setting
url  = 'https://api.binance.com/'
url_p = 'https://fapi.binance.com/'

# # Get Market Data
def GetKline(url, symbol, interval, klinenum):
    if interval[-1]=='m':
        ran = (1000*60)*int(interval.strip(interval[-1])) #time interval of kline(hour) 1000(毫秒)*60(秒)
    if interval[-1]=='h':
        ran = (1000*60*60)*int(interval.strip(interval[-1]))  #time interval of kline(hour) 1000(毫秒)*60(秒)*60(分)
    if interval[-1]=='d':
        ran = (1000*60*60*24)*int(interval.strip(interval[-1]))  #time interval of kline(hour) 1000(毫秒)*60(秒)*60(分)*24(小時)
    if interval[-1]=='w':
        ran = (1000*60*60*24*7)*int(interval.strip(interval[-1]))  #time interval of kline(hour) 1000(毫秒)*60(秒)*60(分)*24(小時)*7(天)
    #time_now= requests.get(url_p + 'fapi/v1/time')
    #print(time_now)
    try:                #request會拿到 開盤時間/開盤價/最高價/最低價/收盤價/成交量/收盤時間/成交額/成交筆數/主動買入成交單/主動買入成交額/忽略參數
        data=[]
        data_int_temp=[]
        if klinenum <=1000:
            data = requests.get(url + 'api/v1/klines', params={'symbol': symbol, 'interval': interval, 'limit': klinenum}).json()
            #print('data=',data)
        if klinenum >1000:
            for num in range (0,klinenum//1000+1):  #ex 2000//1000=2   +1 = 3
                #data_0= requests.get(url_p + 'fapi/v1/klines', params={'symbol': symbol, 'interval': interval, 'limit': klinenum%1000}).json()
                print('===============',num ,sep="\n")
                
                data_0= requests.get(url + 'api/v1/klines', params={'symbol': symbol, 'interval': interval, 'limit': 1000}).json()   #用來抓最近的一根K線時間
                #print('data_0=',data_0)
                data_int= requests.get(url + 'api/v1/klines', params={'symbol': symbol, 'interval': interval,'startTime':data_0[-1][0]-ran*(num*1000+1), 'limit': 1000}).json() #if klinenum=1000→ 算-1000→now if klinenum=2000→算-2000→-1000
                
                data_int_temp=data_int+data_int_temp    #-2000~-1000 + -1000~0
                
                print('datashape=',np.array(data).shape)
                data_int=data_int_temp  #data_int = 可以被整除的數量的K線 1000,2000,3000
                if klinenum%1000 !=0 and num == klinenum//1000:  #抓非1000可整除的剩下K線數  ex 2500→抓後500
                    data_res= requests.get(url + 'api/v1/klines', params={'symbol': symbol, 'interval': interval,'startTime':data_0[-1][0]-ran*(klinenum), 'limit': klinenum%1000}).json() #num from 0 to klinenum//1000
                    data_temp=data_res
                    #print('data_temp_shape0=',np.array(data_temp).shape)
                    data_temp=data_temp+data_int            #除不盡的數量+可以整除的數量
                    #print('data_temp_shape=',np.array(data_temp).shape)
                    data_res = data_temp    #包含可整除部分以及不可整除部分K線
            #print('data=',data_temp)
            if klinenum%1000 == 0:  #k線數量可以被整除
                data = data_int
            else:    
                data = data_res
    except Exception as e:
        print ('Error! problem is {}'.format(e.args[0]))    #報錯
    tmp  = []
    pair = []
    for base in data:
        tmp  = []
        for i in range(0,6):
            if i == 0:  #取得第一項→開盤時間(UNIX時間，單位毫秒)
                timestamp_temp = base[i]
                base[i] = datetime.fromtimestamp(base[i]/1000)  #fromtimestamp(timestamp)→時間戳單位是秒
                #print('basei=',base[i])
            tmp.append(base[i]) #抓出data(因為要處理上放i==0時的時間序列)
        pair.append(tmp)    #data0+data1+data2+....
    df = pd.DataFrame(pair, columns=['date', 'open', 'high', 'low', 'close', 'volume']) #use open/high/low/close/volume for Abstract API to use
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df = df.astype(float)
    #print('data_shape=',np.array(data).shape)
    
    return df



def GetKline_future(url_p, symbol, interval, klinenum):   #(url/交易對/時間區間/K線數量)
    if interval[-1]=='m':
        ran = (1000*60)*int(interval.strip(interval[-1])) #time interval of kline(hour) 1000(毫秒)*60(秒)
    if interval[-1]=='h':
        ran = (1000*60*60)*int(interval.strip(interval[-1]))  #time interval of kline(hour) 1000(毫秒)*60(秒)*60(分)
    if interval[-1]=='d':
        ran = (1000*60*60*24)*int(interval.strip(interval[-1]))  #time interval of kline(hour) 1000(毫秒)*60(秒)*60(分)*24(小時)
    if interval[-1]=='w':
        ran = (1000*60*60*24*7)*int(interval.strip(interval[-1]))  #time interval of kline(hour) 1000(毫秒)*60(秒)*60(分)*24(小時)*7(天)
    #time_now= requests.get(url_p + 'fapi/v1/time')
    #print(time_now)
    try:                #request會拿到 開盤時間/開盤價/最高價/最低價/收盤價/成交量/收盤時間/成交額/成交筆數/主動買入成交單/主動買入成交額/忽略參數
        data=[]
        data_int_temp=[]
        if klinenum <=1000:
            data = requests.get(url_p + 'fapi/v1/klines', params={'symbol': symbol, 'interval': interval, 'limit': klinenum}).json()
            #print('data=',data)
        if klinenum >1000:
            for num in range (0,klinenum//1000+1):  #ex 2050//1000=2   +1 = 3
                #data_0= requests.get(url_p + 'fapi/v1/klines', params={'symbol': symbol, 'interval': interval, 'limit': klinenum%1000}).json()
                print('===============',num ,sep="\n")
                
                data_0= requests.get(url_p + 'fapi/v1/klines', params={'symbol': symbol, 'interval': interval, 'limit': 1000}).json()   #用來抓最近的一根K線時間
                #print('data_0=',data_0)  
                                                                                                               #現在時間
                data_int= requests.get(url_p + 'fapi/v1/klines', params={'symbol': symbol, 'interval': interval,'startTime':data_0[-1][0]-ran*(num*1000+1), 'limit': 1000}).json() #if klinenum=1000→ 算-1000→now if klinenum=2000→算-2000→-1000
                data_int_temp=data_int+data_int_temp    #-2000~-1000 + -1000~0
                print('datashape=',np.array(data).shape)
                data_int=data_int_temp  #data_int = 可以被整除的數量的K線 1000,2000,3000
                if klinenum%1000 !=0 and num == klinenum//1000:  #抓非1000可整除的剩下K線數  ex 2500→抓後500
                    data_res= requests.get(url_p + 'fapi/v1/klines', params={'symbol': symbol, 'interval': interval,'startTime':data_0[-1][0]-ran*(klinenum), 'limit': klinenum%1000}).json() #num from 0 to klinenum//1000
                    data_temp=data_res
                    #print('data_temp_shape0=',np.array(data_temp).shape)
                    data_temp=data_temp+data_int            #除不盡的數量+可以整除的數量
                    #print('data_temp_shape=',np.array(data_temp).shape)
                    data_res = data_temp    #包含可整除部分以及不可整除部分K線
            #print('data=',data_temp)
            if klinenum%1000 == 0:  #k線數量可以被整除
                data = data_int
            else:    
                data = data_res
    except Exception as e:
        print ('Error! problem is {}'.format(e.args[0]))    #報錯
    tmp  = []
    pair = []
    for base in data:
        tmp  = []
        for i in range(0,6):
            if i == 0:  #取得第一項→開盤時間(UNIX時間，單位毫秒)
                timestamp_temp = base[i]
                base[i] = datetime.fromtimestamp(base[i]/1000)  #fromtimestamp(timestamp)→時間戳單位是秒
                #print('basei=',base[i])
            tmp.append(base[i]) #抓出data(因為要處理上放i==0時的時間序列)
        pair.append(tmp)    #data0+data1+data2+....
    df = pd.DataFrame(pair, columns=['date', 'open', 'high', 'low', 'close', 'volume']) #use open/high/low/close/volume for Abstract API to use
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df = df.astype(float)
    print('data_shape=',np.array(data).shape)
    
    return df
# #get the market avg price     #價格為5分鐘的平均值


def GetAvgPrice(url, symbol):
    try:
        price = requests.get(url + 'api/v3/avgPrice', params={'symbol': symbol}).json()['price']
    except Exception as e:
        print ('Error! problem is {}'.format(e.args[0]))
    return float(price)


#Financial indicators

#RSI indicator
def RSI(df, period):
    return abstract.RSI(df, timeperiod=period)
#MA indicator
def MA(df, period):
    return abstract.MA(df, timeperiod=period, matype=0)
#EMA indicator
def EMA(df, period):
    return abstract.EMA(df, timeperiod=period)
#MACD indicator
def MACD(df):
    return abstract.MACD(df,fastpeirod= 12,slowperiod= 26,signalperiod=9) #MACD計算 快線MACD = 12EMA-26EMA 等同國內DIF 線

def remove_nan_find_first_value(index,library):
    temp=index[library]
    initial_list = [x for x in temp if pd.isnull(x) == False]
    initial_first = initial_list[0]
    return initial_first                                                  #慢線 信號線 Signal line =MACD取9日指數移動平均EMA 等同國內MACD線

#KD indicator
def KD(df,fst_period,slwk_period,slwd_period):
            #tradingview     #%K Length      #%K Smoothing                      #%D smoothing
    return abstract.STOCH(df,fastk_period=fst_period, slowk_period=slwk_period, slowk_matype=0, slowd_period=slwd_period, slowd_matype=0)

# # draw
def drawklineticker(token, df,timeset,path,dataset):
    
    #EMA value
    index  = mpf.make_addplot(EMA(df, 20), panel = 0, ylabel = 'EMA20') 
    index2 = mpf.make_addplot(EMA(df, 50), panel = 0, ylabel = 'EMA50')
    #MACD value 
    index3_1=mpf.make_addplot(MACD(df)['macd'],type = 'line',panel = 2,color = 'b', ylabel = 'MACD')
    index3_2=mpf.make_addplot(MACD(df)['macdsignal'],type = 'line',panel = 2,color = 'r')
    index3_3=mpf.make_addplot(MACD(df)['macdhist'],type = 'bar',panel = 2)
    #because the MACD value includes the fast'line',slow'line' and histogram ,use three index to address respectively.
    #RSI value
    index4 = mpf.make_addplot(RSI(df,14), panel = 3,ylabel = 'RSI')

    fig , axes = mpf.plot(df, type = 'candle',style = 'binance', title = token, volume = True,addplot = [index,index2,index3_1,index3_2,index3_3,index4],returnfig=True) #return (1)Figure size XXX with X axex and (2) axex information
    axes[0].legend(('EMA20','EMA50'),loc='upper left')  #mplfinance  legend
    plt.savefig(path+'/'+dataset+ '/' + token + timeset + '.png')
    plt.close()