import json
import pprint

import pandas
import models
from requests import get
from bs4 import BeautifulSoup as bs
from db import SessionLocal, engine
from pydantic import BaseModel 
from models import Stock

import yfinance as yf
from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session

# hdrs =  {"authority": "finance.yahoo.com",
#             "method": "GET",
#             "path": subdoma.format(symbol, start, end),
#             "scheme": "https",
#             "accept": "text/html",
#             "accept-encoding": "gzip, deflate, br",
#             "accept-language": "en-US,en;q=0.9",
#             "cache-control": "no-cache",
#             "dnt": 1,
#             "pragma": "no-cache",
#             "sec-fetch-mode": "navigate",
#             "sec-fetch-site": "same-origin",
#             "sec-fetch-user": "?1",
#             "upgrade-insecure-requests": 1,
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64)"}

import requests_cache
import logging
import requests
from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.DEBUG)

session = requests_cache.CachedSession('yfinance.cache')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
session.headers = headers
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
session.mount('http://', HTTPAdapter(max_retries=retries))



counterYFINANCE=0
counterScrapter=0
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class StockRequest(BaseModel):
    symbol: str



def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def setUpDb():
    global counterYFINANCE,counterScrapter,headers
    #sp500 get symols from wiki url
    print("#################################################################")
    db = SessionLocal()
    resp =  session.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',headers=headers)
    if resp is not None:
            print("######################asd###########")
            soup = bs(resp.text, 'lxml')
            table = soup.find('table', {'class': 'wikitable sortable'})

            for row in table.findAll('tr')[1:]:
                stock = Stock()
                stock.symbol = str(row.findAll('td')[0].text).strip()
                print(stock.symbol)
                # #yahoo api base url
                # url = "https://query1.finance.yahoo.com/v8/finance/chart/"
                # response = get(url+'/'+symbol)
                try:
                    ticker= yf.Ticker(stock.symbol,session=session)
                    stock.name=ticker.info['shortName'] 
                    stock.exchange=ticker.info['exchange']
                    stock.industry=ticker.info['industry']
                    stock.sector=ticker.info['sector']
                    stock.currentPrice=ticker.info['currentPrice']
                  
                except Exception:
                    continue

                #try to get last 30 days closing prices

                try:
                    result= ticker.history(period="1mo")['Close']
                    print(result.empty)
                   
                finally:
                    if(not result.empty):
                            stock.closingPrice = json.loads(result.to_json(orient='index',date_format='iso'))
                            db.add(stock)
                            db.commit()
                            counterYFINANCE=counterYFINANCE+1
                            continue

                # #failure in downloading will try to scrapt from yahoo
                
                pricesUrl= f'https://finance.yahoo.com/quote/{stock.symbol}/history?range=1mo'
                
                req= session.get(pricesUrl,headers=headers)
                if req is not None:
                    soup2 = bs(req.text, 'lxml')
                    priceTable = soup2.find('table',  {'data-test': 'historical-prices'})
                    dataPrices={}
                    for row in priceTable.findAll('tr')[1:]:
                        date=row.findAll('td')[0].text
                        try:
                            closePrice=row.findAll('td')[4].text
                            dataPrices[date] = closePrice
                    
                        finally:
                           continue

                    json_data = json.dumps(dataPrices)
                    
                    stock.closingPrice=json_data
                    counterScrapter=counterScrapter+1
                    db.add(stock)
                    db.commit()


                #could not get last month prices 
                db.add(stock)
                db.commit()

                # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
                # pricesUrl= "https://finance.yahoo.com/quote/"+stock.symbol+"/history?range=1mo"
                # print("$$$$$$$$$$"+pricesUrl+"**********8")
                # req= get(pricesUrl,headers=headers)
           
                # if req is not None:
                #     soup2 = bs(req.text, 'lxml')
                #     print(soup2.prettify())
                #     priceTable = soup2.find('table',  {'data-test':"historical-prices"})
                #     print(priceTable)
                #     dataPrices={}
                #     for row in priceTable.findAll('tr')[1:]:
                #         date=row.findAll('td')[0].text
                #         try:
                #             #some stocks rows have only one dividend culmn
                #             closePrice=row.findAll('td')[4].text
                #             dataPrices[date] = closePrice
        
                #         finally:
                #             continue

                # json_data = json.dumps(dataPrices)
   
                #stock.closingPrice=json_data
                #json.dumps(parsed, indent=4)  
                
                # print(stock.closingPrice)
                # db.add(stock)
                # db.commit()

    print(counterScrapter+"$$$$$$$$$$$$$$$$")
    print(counterYFINANCE+";(;(;(")


# async def addToDb(count: int):
#     global counterYFINANCE,counterScrapter,headers
#     #sp500 get symols from wiki url
#     print("#################################################################")
#     db = SessionLocal()
#     resp =  session.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',headers=headers)
#     if resp is not None:
#             print("######################asd###########")
#             soup = bs(resp.text, 'lxml')
#             table = soup.find('table', {'class': 'wikitable sortable'})

#             for row in table.findAll('tr')[count:]:
#                 stock = Stock()
#                 stock.symbol = str(row.findAll('td')[0]).strip()
#                 print(stock.symbol)
#                 # #yahoo api base url
#                 # url = "https://query1.finance.yahoo.com/v8/finance/chart/"
#                 # response = get(url+'/'+symbol)
#                 try:
#                     ticker= yf.Ticker(stock.symbol,session=session)
#                     stock.name=ticker.info['shortName'] 
#                     stock.exchange=ticker.info['exchange']
#                     stock.industry=ticker.info['industry']
#                     stock.sector=ticker.info['sector']
#                     stock.currentPrice=ticker.info['currentPrice']
                  
#                 except Exception:
#                     continue

#                 #try to get last 30 days closing prices

#                 try:
#                     result= ticker.history(period="1mo")['Close']
#                     print(result.empty)
                   
#                 finally:
#                     if(not result.empty):
#                             stock.closingPrice = json.loads(result.to_json(orient='index',date_format='iso'))
#                             db.add(stock)
#                             db.commit()
#                             counterYFINANCE=counterYFINANCE+1
#                             continue

#                 # #failure in downloading will try to scrapt from yahoo
                
#                 pricesUrl= f'https://finance.yahoo.com/quote/{stock.symbol}/history?range=1mo'
#                 print(type(pricesUrl))
#                 req= session.get(pricesUrl,headers=headers)
#                 if req is not None:
#                     soup2 = bs(req.text, 'lxml')
#                     priceTable = soup2.find('table',  {'data-test': 'historical-prices'})
#                     dataPrices={}
#                     for row in priceTable.findAll('tr')[1:]:
#                         date=row.findAll('td')[0].text
#                         try:
#                             closePrice=row.findAll('td')[4].text
#                             dataPrices[date] = closePrice
                    
#                         finally:
#                            continue

#                     json_data = json.dumps(dataPrices)
                    
#                     stock.closingPrice=json_data
#                     counterScrapter=counterScrapter+1
#                     db.add(stock)
#                     db.commit()


#                 #could not get last month prices 
#                 db.add(stock)
#                 db.commit()

#                 # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
#                 # pricesUrl= "https://finance.yahoo.com/quote/"+stock.symbol+"/history?range=1mo"
#                 # print("$$$$$$$$$$"+pricesUrl+"**********8")
#                 # req= get(pricesUrl,headers=headers)
           
#                 # if req is not None:
#                 #     soup2 = bs(req.text, 'lxml')
#                 #     print(soup2.prettify())
#                 #     priceTable = soup2.find('table',  {'data-test':"historical-prices"})
#                 #     print(priceTable)
#                 #     dataPrices={}
#                 #     for row in priceTable.findAll('tr')[1:]:
#                 #         date=row.findAll('td')[0].text
#                 #         try:
#                 #             #some stocks rows have only one dividend culmn
#                 #             closePrice=row.findAll('td')[4].text
#                 #             dataPrices[date] = closePrice
        
#                 #         finally:
#                 #             continue

#                 # json_data = json.dumps(dataPrices)
   
#                 #stock.closingPrice=json_data
#                 #json.dumps(parsed, indent=4)  
                
#                 # print(stock.closingPrice)
#                 # db.add(stock)
#                 # db.commit()

#     print(counterScrapter+"$$$$$$$$$$$$$$$$")
#     print(counterYFINANCE+";(;(;(")


@app.get("/")
def root(background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    # print(db.query(Stock).count())
    if(not db.query(Stock).first()):
        background_tasks.add_task(setUpDb)
    # elif(db.query(Stock).count()<500):
    #     background_tasks.add_task(addToDb,db.query(Stock).count()+3)
    else:
        stocks = db.query(Stock)
        return stocks.all()


# #import pymysql.cursors
#  Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='eliezer',
#                              database='stocks',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)


# #sp500 get symols from wiki url
# resp = get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

# with connection:
#     with connection.cursor() as cursor:
        
#         if resp is not None:
#             soup = bs(resp.text, 'lxml')
#             table = soup.find('table', {'class': 'wikitable sortable'})

#             for row in table.findAll('tr')[1:]:
#                 symbol = row.findAll('td')[0].text
#                 print(symbol)
#                 # #yahoo api base url
#                 # url = "https://query1.finance.yahoo.com/v8/finance/chart/"
#                 # response = get(url+'/'+symbol)
#                 ticker=yf.Ticker(symbol)
#                 name=ticker.info['shortName']
#                 exchange=ticker.info['exchange']
#                 industry=ticker.info['industry']
#                 sector=ticker.info['sector']
#                 currentPrice=ticker.info['currentPrice']
#                 closingPrice=ticker.history(period="30d")['Close'].values.tolist()

                

#                 sql = "INSERT INTO `sp500` (`symbol`,'name','sector','industry','exchange','lastUpdated','','') VALUES (%s, %s,%s,%s,%s,%s,%s)"
#                 cursor.execute(sql, (symbol,name,sector,industry,exchange,currentPrice,closingPrice ))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()




