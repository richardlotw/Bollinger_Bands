import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
import time

def stock_count():
    global tkcompany, tkdays, revaluelabel, tkdatas, box
    # 獲取微軟股票的歷史數據
    company = tkcompany.get() if tkcompany.get() !='' else '2330.TW'
    days= int(tkdays.get()) if tkdays.get() !='' else 30
    datas= int(tkdatas.get()) if tkdatas.get() !='' else 5
    msft = yf.Ticker(company)
    hist = msft.history(period="max")

    # 計算股票的布林通道
    sma20 = hist["Close"].rolling(window=20).mean()
    std20 = hist["Close"].rolling(window=20).std()
    upper_band = sma20 + 2 * std20
    lower_band = sma20 - 2 * std20
    upper_band_s = sma20 + 1 * std20
    lower_band_s = sma20 - 1 * std20
    print(hist.iloc[len(hist)-2:len(hist)])

    if box.get() =='20日平均線':
        lowpoint = sma20
    elif box.get() =='高通1標準差':
        lowpoint = upper_band_s
    elif box.get() =='低通1標準差':
        lowpoint = lower_band_s
    else:
        lowpoint = lower_band
    # 計算股票成交量的布林通道
    vsma20 = hist["Volume"].rolling(window=20).mean()
    vstd20 = hist["Volume"].rolling(window=20).std()
    vupper_band = vsma20 + 2 * vstd20
    vlower_band = vsma20 - 2 * vstd20
    vupper_band_s = vsma20 + 1 * vstd20
    vlower_band_s = vsma20 - 1 * vstd20


    balance_history = {}

    # 計算策略的報酬率
    balance = 100000  # 初始資金
    stock = 0  # 持有股票數量

    #i-len(hist)+days !=0卡前值不為0

    for i in range(len(hist)-days,len(hist)):
        if hist["Close"].iloc[i] < lowpoint.iloc[i-1] and i-len(hist)+days !=0 and stock == 0:
            # 買入股票
            stock = balance // hist["Close"].iloc[i]
            balance -= stock * hist["Close"].iloc[i]
            print(i-len(hist)+days," ", hist["Close"].iloc[i])
        elif hist["Close"].iloc[i] > upper_band.iloc[i-1] and i-len(hist)+days !=0 and stock > 0:
            # 賣出股票
            balance += stock * hist["Close"].iloc[i]
            stock = 0
            print(i-len(hist)+days," ", hist["Close"].iloc[i])
        
        balance_history[hist.index[i]] = (balance + stock * hist['Close'].iloc[i])

    # 計算最終的報酬率
    final_value = balance + stock * hist["Close"].iloc[-1]
    return_rate = (final_value - 100000) / 100000
    print("最終報酬率：%.2f%%" % (return_rate * 100))
    revaluelabel.config(text=str(round(float(return_rate * 100),2))+'%')

    #plot the loss and accuracy
    N = days
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, N), hist["Close"].iloc[len(hist)-days:len(hist)], 'o-',label="Close")
    plt.plot(np.arange(0, N), upper_band.iloc[len(hist)-days:len(hist)], label="UPPER")
    plt.plot(np.arange(0, N), lower_band.iloc[len(hist)-days:len(hist)], label="LOWER")
    plt.plot(np.arange(0, N), sma20.iloc[len(hist)-days:len(hist)], label="MEAN")
    plt.plot(np.arange(0, N), upper_band_s.iloc[len(hist)-days:len(hist)], label="UPPER_1s")
    plt.plot(np.arange(0, N), lower_band_s.iloc[len(hist)-days:len(hist)], label="LOWER_1s")


    for i in range(days-datas,days):
        j = i + len(hist)-days
        plt.text(i-0.7,round(hist["Close"].iloc[j])+0.5,round(hist["Close"].iloc[j],2),fontsize=6)

    plt.text(i-0.7,round(upper_band.iloc[j])+0.2,round(upper_band.iloc[j],2),fontsize=6)
    plt.text(i-0.7,round(sma20.iloc[j])+0.5,round(sma20.iloc[j],2),fontsize=8)
    plt.text(i-0.7,round(lower_band.iloc[j])+0.2,round(lower_band.iloc[j],2),fontsize=6)
    plt.text(i-0.7,round(upper_band_s.iloc[j])+0.2,round(upper_band_s.iloc[j],2),fontsize=6)
    plt.text(i-0.7,round(lower_band_s.iloc[j])+0.2,round(lower_band_s.iloc[j],2),fontsize=6)


    plt.title(company)
    plt.xlabel("Days#")
    plt.ylabel("Price")
    t = time.localtime()
    num = str(t.tm_year)+str(t.tm_mon)+str(t.tm_mday)+str(t.tm_min)+str(t.tm_sec)
    print(num)
    plt.legend()
    plt.savefig(company+'price'+num+'.png')
    # plt.show()

    N = days
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, N), hist["Volume"].iloc[len(hist)-days:len(hist)], 'o-',label="Volume")
    plt.plot(np.arange(0, N), vupper_band.iloc[len(hist)-days:len(hist)], label="vUPPER")
    plt.plot(np.arange(0, N), vsma20.iloc[len(hist)-days:len(hist)], label="vMEAN")
    plt.plot(np.arange(0, N), vlower_band.iloc[len(hist)-days:len(hist)], label="vLOWER")
    # plt.plot(np.arange(0, N), vupper_band_s.iloc[len(hist)-days:len(hist)], label="vUPPER_1s")
    # plt.plot(np.arange(0, N), vlower_band_s.iloc[len(hist)-days:len(hist)], label="vLOWER_1s")

    for i in range(days-datas,days):
        j = i + len(hist)-days
        plt.text(i-0.7,round(hist["Volume"].iloc[j])+0.5,round(hist["Volume"].iloc[j],2),fontsize=6)

    plt.text(i-0.7,round(vupper_band.iloc[j])+0.2,round(vupper_band.iloc[j],2),fontsize=6)
    plt.text(i-0.7,round(vsma20.iloc[j])+0.5,round(vsma20.iloc[j],2),fontsize=6)
    plt.text(i-0.7,round(vlower_band.iloc[j])+0.2,round(vlower_band.iloc[j],2),fontsize=6)
    # plt.text(i-0.7,round(vupper_band_s.iloc[j])+0.5,round(vupper_band_s.iloc[j],2),fontsize=8)
    # plt.text(i-0.7,round(vlower_band_s.iloc[j])+0.5,round(vlower_band_s.iloc[j],2),fontsize=8)


    plt.title(company)
    plt.xlabel("Days#")
    plt.ylabel("Volume")

    plt.legend()
    plt.savefig(company+"volume"+num+'.png')
    plt.show()


def main():
    global tkcompany, tkdays, revaluelabel, tkdatas, box
    #介面程式
    window = tk.Tk() #tkinten
    window.title('AI_StockWay') #介面的名字
    window.geometry('1024x768')   #視窗大小
    window['bg']='#D14152' #顏色

    companylabel= tk.Label(window, text='公司代號(Company):',font=('Arial',16), width=16, height=2, bg = 'khaki') 
    companylabel.grid(column = 0, row=0, padx = 5, pady = 5)

    tkcompany = tk.StringVar()
    tkcom = tk.Entry(window, textvariable=tkcompany, font = ('Arial', 16))
    #tkcom.place(x = column1, y=row1, width = 140, height = 30)
    tkcom.grid(column=1, row=0, padx = 5, pady = 5)

    dayslabel= tk.Label(window, text='天數(Days):',font=('Arial',16), width=16, height=2, bg = 'khaki') 
    dayslabel.grid(column = 0, row=1, padx = 5, pady = 5)

    tkdays = tk.StringVar()
    tkday = tk.Entry(window, textvariable=tkdays, font = ('Arial', 16))
    #tkcom.place(x = column1, y=row1, width = 140, height = 30)
    tkday.grid(column=1, row=1, padx = 5,pady = 5)

    dataslabel= tk.Label(window, text='筆數(Datas):',font=('Arial',16), width=16, height=2, bg = 'khaki') 
    dataslabel.grid(column = 0, row=2, padx = 5, pady = 5)

    tkdatas = tk.StringVar()
    tkdata = tk.Entry(window, textvariable=tkdatas, font = ('Arial', 16))
    #tkcom.place(x = column1, y=row1, width = 140, height = 30)
    tkdata.grid(column=1, row=2, padx = 5,pady = 5)



    tkcount = tk.Button(window, text="運算", font=('Arial',18), width=4, height=2, bg='khaki', command = stock_count)
    tkcount.grid(column=1, row=5, padx = 5,pady = 5)

    returnlabel= tk.Label(window, text='最終報酬(Return):',font=('Arial',16), width=16, height=2, bg = 'khaki') 
    returnlabel.grid(column = 0, row=4, padx = 5, pady = 5)

    revaluelabel= tk.Label(window, text='%',font=('Arial',16), width=10, height=2, bg = 'khaki') 
    revaluelabel.grid(column = 1, row=4, padx = 5, pady = 5)


    boxlabel= tk.Label(window, text='低點選擇',font=('Arial',16), width=10, height=2, bg = 'khaki')
    boxlabel.grid(column = 0, row=3, padx = 5, pady = 5) 
    box = ttk.Combobox(window, width='15', value=['高通1標準差','20日平均線', '低通1標準差','低通道'], font = ('Arial', 16))
    box.grid(column = 1, row=3, padx = 5, pady = 5)
    window.mainloop()

if __name__ == '__main__':
    main()
