from email import header
from fileinput import close
import json
from pprint import pprint
import requests

from bs4 import BeautifulSoup as bs

import requests
from requests.adapters import HTTPAdapter



# html = '''<table class="W(100%) M(0)" data-test="historical-prices" data-reactid="33">
#     <thead data-reactid="34">
#         <tr class="C($tertiaryColor) Fz(xs) Ta(end)" data-reactid="35">
#             <th class="Ta(start) W(100px) Fw(400) Py(6px)" data-reactid="36"><span data-reactid="37">Date</span></th>
#             <th class="Fw(400) Py(6px)" data-reactid="38"><span data-reactid="39">Open</span></th>
#             <th class="Fw(400) Py(6px)" data-reactid="40"><span data-reactid="41">High</span></th>
#             <th class="Fw(400) Py(6px)" data-reactid="42"><span data-reactid="43">Low</span></th>
#             <th class="Fw(400) Py(6px)" data-reactid="44"><span data-reactid="45">Close*</span></th>
#             <th class="Fw(400) Py(6px)" data-reactid="46"><span data-reactid="47">Adj Close**</span></th>
#             <th class="Fw(400) Py(6px)" data-reactid="48"><span data-reactid="49">Volume</span></th>
#         </tr>
#     </thead>
#     <tbody data-reactid="50">
#         <tr class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)" data-reactid="51">
#             <td class="Py(10px) Ta(start) Pend(10px)" data-reactid="52"><span data-reactid="53">Oct 10, 2019</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="54"><span data-reactid="55">2,918.55</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="56"><span data-reactid="57">2,948.46</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="58"><span data-reactid="59">2,917.12</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="60"><span data-reactid="61">2,938.13</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="62"><span data-reactid="63">2,938.13</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="64"><span data-reactid="65">3,217,250,000</span></td>
#         </tr>
#         <tr class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)" data-reactid="66">
#             <td class="Py(10px) Ta(start) Pend(10px)" data-reactid="67"><span data-reactid="68">Oct 09, 2019</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="69"><span data-reactid="70">2,911.10</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="71"><span data-reactid="72">2,929.32</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="73"><span data-reactid="74">2,907.41</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="75"><span data-reactid="76">2,919.40</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="77"><span data-reactid="78">2,919.40</span></td>
#             <td class="Py(10px) Pstart(10px)" data-reactid="79"><span data-reactid="80">2,726,820,000</span></td>
#         </tr>
# </table>'''
# soup = bs(html, 'lxml')
# index = [th.text for th in soup.select('[data-test="historical-prices"] th')].index('Close*') + 1
# print(index)
# data = [td.text for td in soup.select(f'[data-test="historical-prices"] td:nth-of-type({index})')]
# print(data)
print(3+3)

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
# pricesUrl= "https://finance.yahoo.com/quote/"+"MMM"+"/history?range=1mo"
# req= requests.get(pricesUrl,headers=headers)
# if req is not None:
#     soup2 = bs(req.text, 'lxml')
#     priceTable = soup2.find('table',  {'data-test': 'historical-prices'})
#     dataPrices={}
#     for row in priceTable.findAll('tr')[1:]:
#         date=row.findAll('td')[0].text
#         try:
#             closePrice=row.findAll('td')[4].text
#             dataPrices[date] = closePrice
        
#         finally:
#              continue

#     json_data = json.dumps(dataPrices)
#     print(json_data)
import yfinance as yf
stock="appl"

msft = yf.Ticker("BRK.B").info
print(msft)

# result= msft.history(period="1mo")['Close']
# print(result.to_json(date_format='iso'))
# # print("@@@@@@@@@@@@@@@@@@@@@@@@@@22")
# print(result)
# parsed = json.loads(result.to_json(orient='index',date_format='iso'))
# print("((((((((((((((((((((((((")
# print(parsed)
# closingPrice=json.dumps(parsed, indent=4)  
# # print("sssssssssssssssssssssssssssssssss")
# # print(closingPrice)
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
# symbol = "MMM"
# req= requests.get("https://query1.finance.yahoo.com/v8/finance/chart/"+symbol+"?interval=1m",headers=headers).json()
# print(req['chart']['result'][0]['indicators']['quote'][0]['close'])



#from requests.packages.urllib3.util.retry import Retry


# session = requests.Session()
# retry = Retry(connect=3, backoff_factor=0.5)
# adapter = HTTPAdapter(max_retries=retry)
# session.mount('http://', adapter)
# session.mount('https://', adapter)

# # session.get(url)

# proxies = {'http':'http://user:pswd@foo-webproxy.foo.com:7777', 'https':'http://user:pswd@foo-webproxy.foo.com:7777'}

# def save_sp500_tickers():
#     resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
#     soup = BeautifulSoup(resp.text, 'lxml')
#     table = soup.find('table', {'class': 'wikitable sortable'})
#     tickers = []
#     for row in table.findAll('tr')[1:]:
#         ticker = row.findAll('td')[0].text
#         tickers.append(ticker)
#         print(ticker)

# #save_sp500_tickers()

# #import yfinance as yf

# #msft = yf.Ticker("MSFT")

# # get stock info
# #msft.info()

# # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

# # #html = requests.get("https://www.spglobal.com/spdji/en/indices/equity/sp-500/#index-linked-product",headers=headers)

# # html=requests.get('https://fxp.co.il/')
# # soup = BeautifulSoup(html.content, 'html.parser')
# # pprint(soup.prettify())

# # #yahoo api base url
# # url = "https://query1.finance.yahoo.com/v8/finance/chart/"
# # stocksymbol='appl'
# # closingpriceurl ='https://finance.yahoo.com/quote/W/history?p='+stocksymbol
# # html=requests.get(closingpriceurl,proxies=proxies,headers=headers)
# # print(html.content)
# # print(html.content)
# # soup = BeautifulSoup(html.content, 'html.parser')


# # # print(soup.prettify())


# import bs4
# import requests
    
# import pymysql.cursors

# # Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='eliezer',
#                              database='stocks',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# 

# with connection:
#     with connection.cursor() as cursor:
        
#         if resp is not None:
#             soup = BeautifulSoup(resp.text, 'lxml')
#             table = soup.find('table', {'class': 'wikitable sortable'})

#             for row in table.findAll('tr')[1:]:
#                 symbol = row.findAll('td')[0].text
#                 sector=row.findAll('td')[3].text
#                 print(symbol+sector)
#                 sql = "INSERT INTO `sp500` (`symbol`,'sector') VALUES (%s, %s)"
#                 cursor.execute(sql, (symbol, sector))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
