# CCPNS user manual
- **CCPNS** stand for CryptoCurrency Price Notification System
- [Github](https://github.com/chiangkd/CCPNS)
## 動機

目前市面上最多使用者用來查看虛擬貨幣行情的網站為 [TradingView](https://tw.tradingview.com/)，而行情提醒以及分割畫面為該網站的付費功能，在虛擬貨幣交易所中，不同於台灣股票市場，一般行情 API 為 24 小時免費提供，故利用 Python 來撰寫相關功能程式。

## 簡介
- 程式剛運行時會在 command window 上顯示 `drawing XXXXXXX` 等字樣，等待一陣子後 GUI 就會啟動
- 在程式運行過程中如果遇到整點(圖表需要更新，程式會暫時停止運作，靜待圖表更新完成後繼續運行)

**目前功能**
- [x] 分割畫面同時顯不同幣種
- [x] 連接 Line 進行行情提醒(透過 IFTTT key)
- [x] 新增不同幣種行情提醒

**指標**
- [x] RSI
- [X] MACD

**待補功能**
- [ ] 各類技術指標行情提醒 (80/100%)
- [ ] 滾動式圖表

**主介面**
![](https://i.imgur.com/WYmmOZH.png)




## 所需封包

- os
- [TA-Lib](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)
- tkinter
- PIL
- matplotlib
- time
- pandas
- request
- numpy
- datetime
- [mplfinance](https://github.com/matplotlib/mplfinance)

## 修改指南

- 若要新增幣種則可以在 `gui.py` 的 `line 885` 進行手動新增，因程式運行效能暫時僅有 4 個幣種
    - 不建議修改時區，業者可能並沒有提供對應 API
```python
coin_list = ["BTCUSDT","ETHUSDT","LTCUSDT","ADAUSDT"]#define token list used in change img label
time_list = ["5m","15m","30m","1h","4h","1d"]
```

- 當前使用的 API 為 [幣安Binance](https://binance-docs.github.io/apidocs/spot/en/#change-log)
```python
url  = 'https://api.binance.com/'
url_p = 'https://fapi.binance.com/'
```
- 若要修改為其他交易所的 API 諸如 OKEx、bybit ，可以查找該交易所的行情 API 取代位於 `market.py` `line 21 & 22` 的網址即可。
    - `url` 為**現貨**行情
    - `url_p` 為**永續合約**合約行情

- 若要修改顯示的 K 線數目，可以修改位於 `gui.py` `line 651` 的 `klinenum` 變數
    - **日後應修改成由介面操作**

- 預設顯示為 **現貨價格** 若要改為 **永續合約** 價格，可以將位於 `gui.py` `line 655` 的 `GetKline` 函式修改為 `GetKline_future`
    - `GetKline` 為**現貨價格**
    - `GetKline_future` 為**永續合約**價格
## 視窗


### 單一視窗

- 左上角可供選擇不同幣種 / 時間區間
- 右上角灰色區塊為**即時行情**
![](https://i.imgur.com/O6kAMZl.png)

![](https://i.imgur.com/gBNQHdf.png)

### 分割視窗顯示不同幣種/時間區間

![](https://i.imgur.com/nqP3iRp.png)


## IFTTT key setting

[如何創建 IFTTT KEY](https://www.oxxostudio.tw/articles/201803/ifttt-line.html)

如果創建好之後找不到 key 在哪裡 點選 IFTTT explore 搜尋 webhooks 點選 documentation 就可以找到 key 囉
![](https://i.imgur.com/Wu5vB9d.png)

創建好之後把 key 貼在藍色區塊中按下 enter
![](https://i.imgur.com/ipp7onR.png)

成功連接LINE應該會跳通知
![](https://i.imgur.com/U8fBFPW.png)

## 行情提醒

IFTTT KEY 連接成功之後右下角的綠色區塊可以設定提醒行情(高於某個價格提醒，提醒時間間隔)
![](https://i.imgur.com/smNKhhC.png)

就會有提醒拉~~

![](https://i.imgur.com/nWgnx8Z.png)



