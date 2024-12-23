import requests
from bs4 import BeautifulSoup as Bs
import customtkinter as ctk
from customtkinter import CTkButton as btn
from customtkinter import CTkCheckBox as FFlag
from fake_useragent import UserAgent
from threading import Thread
from time import sleep



class Parser:
        def bybit(self, link):
            with requests.get(link, headers={'User-Agent': UserAgent().random}) as response:
                soup = Bs(response.content, 'lxml')
                bybit_price = soup.find('div', class_='card-info-price').text
                bybit_percent = soup.find('div', class_='card-info-percent').text
            return {'bybit':{'price':bybit_price,
                    'percent':bybit_percent}}
              
        def binance(self, link):
            with requests.get(link, headers={'User-Agent': UserAgent().random}) as response:
                soup = Bs(response.content, 'lxml')
                price = soup.find('span', class_='t-subtitle2 text-textPrimary md:t-subtitle1 lg:t-headline5').text.strip('1 Bitcoin equals USD')
                try:
                    percent = soup.find('span', class_='t-subtitle2 md:t-subtitle1 lg:t-headline5 text-sell').text
                except Exception as ex:
                    percent = soup.find('span', class_='t-subtitle2 md:t-subtitle1 lg:t-headline5 text-buy').text

            return {'binance':{'price':price,
                 'percent':percent}}
       
        def okx(self, link):
            with requests.get(link, headers={'User-Agent': UserAgent().random}) as response:
                soup = Bs(response.content, 'lxml')
                price = soup.find('div', class_='index_price__VXAhl').text
                percent = soup.findAll('div', class_='index_changePercentage__3MkFY')[1].text.strip('()')
            return {'okx':{'price':price,
                    'percent':percent}}
        
        
        def btc(self):
                bybit = self.bybit('https://www.bybit.com/ru-RU/coin-price/bitcoin/')
                okx = self.okx('https://www.okx.com/ru/price/bitcoin-btc')
                binance = self.binance('https://www.binance.com/ru/price/bitcoin')
                a = {'btc': [bybit, okx, binance]}
                return a

        def eth(self):
                bybit = self.bybit('https://www.bybit.global/en/coin-price/ethereum/')
                okx = self.okx('https://www.okx.com/ru/price/ethereum-eth')
                binance = self.binance('https://www.binance.com/ru/price/ethereum')
                a = {'eth': [bybit, okx, binance]}
                return a

        def bnb(self):
                bybit = self.bybit('https://www.bybit.com/ru-RU/coin-price/binancecoin/')
                okx = self.okx('https://www.okx.com/ru/price/bnb-bnb')
                binance = self.binance('https://www.binance.com/ru/price/bnb')
                a = {'bnb': [bybit, okx, binance]}
                return a

        def xrp(self):
                bybit = self.bybit('https://www.bybit.global/en/coin-price/ripple/')
                okx = self.okx('https://www.okx.com/ru/price/xrp-xrp')
                binance = self.binance('https://www.binance.com/ru/price/xrp')   
                a = {'xrp': [bybit, okx, binance]}
                return a

        def Activity(self):
            results = {}
            threads = [
                Thread(target=lambda: results.update(self.xrp())),
                Thread(target=lambda: results.update(self.bnb())),
                Thread(target=lambda: results.update(self.btc())),
                Thread(target=lambda: results.update(self.eth()))
            ]

            for i in threads:
                i.start()

            for i in threads:
                i.join()
            
            return results
            


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.parser = Parser()
        results = self.parser.Activity()
        #threads = [
        #    Thread(target=lambda: results.update(parser.btc())),
        #    Thread(target=lambda: results.update(parser.eth())),
        #    Thread(target=lambda: results.update(parser.bnb())),
        #    Thread(target=lambda: results.update(parser.xrp()))
        #]
        #self.btc = parser.btc()
        #self.bnb = parser.bnb()
        #self.eth = parser.eth()
        #self.xrp = parser.xrp()
        #for thread in threads:
        #    thread.start()
            
        #for thread in threads:
        #    thread.join()
        
        print(results)

        self.btc = results['btc']
        self.bnb = results['bnb']
        self.xrp = results['xrp']
        self.eth = results['eth']
        
        
        
        self.geometry('800x300')
        self.resizable(False, False)
        self.choice()
        self.frame()
        self.inf = []
    # 0 - bybit 1 - okx 2 - binance
    def choice(self):
        frame = ctk.CTkFrame(self, width=100)
        frame.pack(side='left', fill=ctk.Y)

        flagBTC = ctk.CTkCheckBox(frame, command=lambda:self.information(flagBTC, binance=self.btc[2]['binance'], okx=self.btc[1]['okx'], bybit=self.btc[0]['bybit']), text='BTC')
        flagBTC.pack()

        flagETH = FFlag(frame, command=lambda:self.information(flagETH, binance=self.eth[2]['binance'], okx=self.eth[1]['okx'], bybit=self.eth[0]['bybit']), text='ETH')
        flagETH.pack()

        flagBNB = FFlag(frame, command=lambda:self.information(flagBNB, binance=self.bnb[2]['binance'], okx=self.bnb[1]['okx'], bybit=self.bnb[0]['bybit']), text='BNB')
        flagBNB.pack()

        flagXRP = FFlag(frame, command=lambda:self.information(flagXRP, binance=self.xrp[2]['binance'], okx=self.xrp[1]['okx'], bybit=self.xrp[0]['bybit']), text='XRP')
        flagXRP.pack()

        #flagTether = FFlag(frame, command=lambda:self.information(flagTether), text='USDt')
        #flagTether.pack()


    def information(self, a, binance=None, bybit=None, okx=None):
        coin = a._text
        if a.get():
            if coin not in self.inf:
                info = ctk.CTkFrame(self.first, height=70)
                #self.reload_ = ctk.CTkButton(info, text='reload', width=5, command=lambda: self.reloadFrame('BTC'))
                text = ctk.CTkLabel(info, font=('Arial', 15), text=f'||      {coin}     ||    {bybit['price']} {bybit['percent']}    ||    {binance['price']} {binance['percent']}    ||     {okx['price']} {okx['percent']}||')

                info.pack(fill=ctk.X, padx=5, pady=5)
                #self.reload_.pack(side='left')
                text.pack(side='left')
                self.inf.append([coin, info])
        else:    
            for i in self.inf:
                if coin in i:
                    i[1].destroy()
                    self.inf.remove(i)
                    #self.reload_.destroy()
                    break
                    

    def frame(self):
        self.first = ctk.CTkFrame(self)
        self.first.pack(fill=ctk.BOTH, padx=5, pady=5, expand=True)

        second = ctk.CTkFrame(self.first, height=50)
        second.pack(fill=ctk.X, padx=5, pady=5)

        text = ctk.CTkLabel(second, text='|| Название ||      bybit      ||     binance      ||     okx      ||', font=('Arial', 24))
        text.pack(side='left')

    


        



if __name__ == '__main__':
    app = App()
    app.mainloop()
    
