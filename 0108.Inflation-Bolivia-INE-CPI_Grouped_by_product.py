#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
from datetime import datetime


import requests
from lxml import etree
from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[16]:


url = "https://www.ine.gob.bo/index.php/nacional/"

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

req = Request(url)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    if 'Índice a nivel Productos' in link.get_text():
        links.append(link.get('href'))


# In[17]:


df = pd.read_excel(links[0], sheet_name = 'Bolivia', skiprows=4)
df = df.rename(columns={'DESCRIPCIÓN': 'Date'})
df = df[df.columns[1:]]
df = df.set_index('Date')
df = df.dropna(how='all')
df = df.T
df = df.rename(columns={'ÍNDICE GENERAL': 'Nivel general - Indice de precios'})
df['country'] = 'Bolivia'


# In[18]:


df['Date']= df.index
df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
df = df.set_index('Date')


alphacast.datasets.dataset(108).upload_data_from_df(df, 
                 deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

# In[ ]:




