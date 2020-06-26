#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import sqlite3
import argparse

def database(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("CREATE TABLE Billboard200 (ThisWeekRank TEXT , Name TEXT, Artist TEXT,LastWeekRank TEXT, PeakRank TEXT, Duration TEXT )" )
    conn.close()

def upload(info,dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("INSERT INTO Billboard200 VALUES(?,?,?,?,?,?)",info)
    conn.commit()
    conn.close()
    
dbname = 'BillboardAlbum200.db'

database(dbname)

billboard200_url = "https://www.billboard.com/charts/billboard-200"


url = requests.get (billboard200_url)
soup = BeautifulSoup (url.content,'html.parser')  
albums200 = soup.find_all ("button", {"class": "chart-element__wrapper"})
for album in albums200 :
    albums = {}
    albums ["ThisWeekRank"] = album.find ("span", {"class" : "chart-element__rank__number"}).text
    albums ["Name"] = album.find ("span", {"class" : "chart-element__information__song"}).text
    albums ["Artist"] = album.find ("span", {"class" : "chart-element__information__artist"}).text
    albums ["LastWeekRank"] = album.find ("div", {"class" : "chart-element__meta text--last"})
    if albums ["LastWeekRank"] != None:
        albums ["LastWeekRank"]=albums ["LastWeekRank"].text
    else:
        albums ["LastWeekRank"] = None
    albums ["PeakRank"] = album.find ("div", {"class" : "chart-element__meta text--peek"})
    if albums ["PeakRank"] != None:
        albums ["PeakRank"]=albums ["PeakRank"].text
    else:
        albums ["PeakRank"] = None
    albums ["Duration"] = album.find ("div", {"class" : "chart-element__meta text--week"})
    if albums ["Duration"] != None:
        albums ["Duration"]=albums ["Duration"].text
    else:
        albums ["Duration"] = None

    
    information = tuple(albums.values())
    upload (information,dbname)


# In[3]:


import sqlite3
conn  = sqlite3.connect ('Billboard.db')
cur = conn.cursor ()
x = cur.execute ("SELECT * FROM Billboard200")

for i in x :
    print (i)
    
conn.commit ()
conn.close ()


# In[ ]:




