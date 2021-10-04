# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 14:31:24 2021

@author: neera
"""


import time
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import json

class upstox_oc :
    def __init__(self, path):
        
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        try:
            self.driver = webdriver.Chrome(path,options=option)
        except:
            raise Exception ("Please enter correct path to ChromeDriver. ")
        self.data = pd.DataFrame()
    
    def login(self, userid, password, twofa): 
        url = "https://login-v2.upstox.com/?&client_id=PW3-6Agd37PB52Q6B6DDpYWLuT7b&platform_id=PW3&redirect_path=%2F&redirect_query=e30%3D&redirect_uri=https%3A%2F%2Fpro.upstox.com"
        self.driver.get(url)
        elementID = self.driver.find_element_by_id('userCode')
        elementID.send_keys(userid)
        
        elementID = self.driver.find_element_by_name('password')
        elementID.send_keys(password)
        
        elementID.submit()
        
        time.sleep(2)
        elementID = self.driver.find_element_by_id('yob')
        elementID.send_keys(twofa)
        time.sleep(2)
        if self.driver.page_source.find("Funds") == -1 :
            raise Exception ("Unable to Login")
    
    def get_oc(self, symbol):
        if symbol == "NIFTY" : 
            self.exc = "NSE_INDEX"
            self.symbol = "Nifty%2050"
        elif symbol == "BANKNIFTY":
            self.exc = "NSE_INDEX"
            self.symbol = "Nifty%20Bank"
        else :
            self.exc = "NSE_EQ"
            self.symbol = symbol
        
        url = 'https://pro.upstox.com/option-chain/'+self.exc+'/'+self.symbol
        
        self.driver.get(url)
        time.sleep(1.5)
        src = self.driver.page_source
        soup = BeautifulSoup(src,'lxml')
        table = soup.find_all('table' ,{'class':'_3bopz0b9l67Nwoyu8pEQp3 _1VLPB0y20VYNdykG8_HKnT'}) 
        dets = {}
        for x in range(len(table)): 
            row = table[x].find_all('tr')
            dets[x] = {}
            n = 0
            if x == 0 : 
                for i in range(1, len(row)):   
                    try: 
                        cell = row[i].find_all('td')
                        oit = cell[0].find_all('div')
                        oi = oit[0].get_text().replace(",", "")
                        oich = oit[1].get_text().replace(",", "")
                        oichper = cell[1].find_all('div')[0].get_text().replace("%", "")
                        vol = cell[2].find_all('div')[0].get_text().replace(",", "")
                        iv = cell[3].find_all('div')[0].get_text().replace(",", "")
                        bid = cell[4].find_all('div')[0].get_text().replace(",", "")
                        ask = cell[5].find_all('div')[0].get_text().replace(",", "")
                        ltp = cell[6].find_all('div')[1].get_text().replace(",", "")
                        ltpch = cell[6].find_all('div')[2].get_text().replace(",", "")
                        dets[x][n] = {"ce_oitot":oi, "ce_oich" : oich, "ce_oichper" :oichper, "ce_volume" : vol, "ce_iv": iv, "ce_bid": bid,"ce_ask": ask, "ce_ltp": ltp, "ce_ltpch": ltpch }
                        n = n+1
                    except:
                        pass
            else : 
                for i in range(1, len(row)):   
                    try: 
                        cell = row[i].find_all('td')
                        oit = cell[7].find_all('div')
                        oi = oit[0].get_text().replace(",", "")
                        oich = oit[1].get_text().replace(",", "")
                        oichper = cell[6].find_all('div')[0].get_text().replace("%", "")
                        vol = cell[5].find_all('div')[0].get_text().replace(",", "")
                        iv = cell[4].find_all('div')[0].get_text().replace(",", "")
                        bid = cell[3].find_all('div')[0].get_text().replace(",", "")
                        ask = cell[2].find_all('div')[0].get_text().replace(",", "")
                        ltp = cell[1].find_all('div')[1].get_text().replace(",", "")
                        ltpch = cell[1].find_all('div')[2].get_text().replace(",", "")
                        dets[x][n] = {"pe_oitot":oi, "pe_oich" : oich, "pe_oichper" :oichper, "pe_volume" : vol, "pe_iv": iv, "pe_bid": bid,"pe_ask": ask, "pe_ltp": ltp, "pe_ltpch": ltpch }
                        n = n+1
                    except:
                        pass
            
        table = soup.find_all('table' ,{'class':'_3bopz0b9l67Nwoyu8pEQp3 _1VLPB0y20VYNdykG8_HKnT _3nYyUsIA6U4EQxrx70lYLH'})
        row = table[0].find_all('tr')
        
        dets[2] = {}
        n = 0 
        for i in range(len(row)) : 
            try: 
                cell = row[i].find_all('td')
                stk = cell[0].find_all('div')[0].get_text().replace(",", "")
                try : 
                    stk1 = int(stk.strip()[0]) 
                    dets[2][n] = {"strike" :stk }
                    n = n+1
                except: 
                    cp = stk.split()[1].replace(",", "")
                    pass
            except:
                pass
        
        df = pd.DataFrame()
        for i in dets: 
            df1 = pd.DataFrame.from_dict(dets[i]).transpose()
            df = pd.concat([df, df1], axis=1)
        self.data = df
        df['stk'] = df['strike']
        df = df.set_index('stk')
        result = df.to_json(orient="index")
        self.optchain = json.loads(result)
        self.optchain['spot'] = cp
        return self.optchain
    
    def close(self):
        self.driver.close()
        


    