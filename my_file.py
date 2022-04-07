import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.bauteilclick.ch"
r = requests.get(URL) 
soup = BeautifulSoup(r.content, 'html.parser')

urls_to_scrape = []

boh = soup.find('nav',attrs={'class':'btc-sidebar-navigation toggable'}).findAll("li",attrs={"class":'has-children'})
for i in boh:
    urls_to_scrape.append(URL + i.find('a',attrs={'class':'link'},href=True)["href"])
    
    
rest_info = []
for i in urls_to_scrape:
    URL = i + "?page=0"
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html.parser')
    acco = soup.find('nav', attrs = {'class':'paging'})
    
    calc_npages = [s for s in acco.text.split(" ") if s.isdigit()]
    if not calc_npages:
        continue
    else:
        num_pages = max([s for s in acco.text.split(" ") if s.isdigit()])

    for j in range(0,int(num_pages)):
        URL = i + "?page="+str(j)
        r = requests.get(URL) 
        soup = BeautifulSoup(r.content, 'html.parser') 

        #get object type
        type_obj = URL.split('kaufen/')[1].split(".")[0]
        table = soup.findAll('article', attrs = {'class':'ym-clearfix article'}) 
        for row in table:

            #get prices
            buy_info = row.find('div',attrs={'class':'ym-gr article-buy'})
            price = buy_info.find('p',attrs={'class':'price'}).find('span').text

            #get name
            name_info = row.find('div',attrs={'class':'ym-gl article-info'})
            name = name_info.find('h2',attrs={'class':'t-h2'}).find('a').text

            number = name_info.findAll('p')[1].text

            quantity = name_info.find('p',attrs={'class':'quantity'}).text
            provider = name_info.find('p',attrs={'class':'provider'}).text
            rest_info.append([type_obj,name,number,price,quantity,provider,datetime.today().strftime('%Y-%m-%d')])
            
            
df = pd.DataFrame(rest_info, columns = ['Type','Name', 'Number','Price','Quantity','Provider','Date'])
df.to_csv("test.csv",mode='a', index=False, header=False)
