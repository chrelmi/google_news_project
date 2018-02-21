#!/usr/bin/env python3
import newspaper
import re
import csv
import sys
import psycopg2
from geopy.geocoders import Nominatim
import folium
import time
paper=newspaper.build('https://news.google.com/news/?ned=it&gl=IT&hl=it')
key="la"
sent=0
found=0
coordinate=[]
c=0
map_osm = folium.Map(location=[41.903853, 12.484492],zoom_start=6,tiles='CartoDB dark_matter')
for article in paper.articles: #download,replace e assegnazione degli articoli
	print(article.url)
	url=article.url
	text=article.text
	text=text.lower()
	textprint=str(text)
	text=text.split()
	tit=article.title
	title=str(tit)
	title=title.lower()
	link=str(url)
	print (title)
	title=title.replace(",","")
	title=title.replace(".","")
	title=title.replace(":","")
	title=title.replace(";","")
	title=title.replace("?","")
	title=title.replace("!","")
	title=title.split()
	date=article.publish_date
	date=str(date)
	print (date)
	print (title)
	if key in title:
		print (title)
		sent=1
	with open('paesi.csv') as csvfile: #estrazione della città tramite un confronto con il file CSV di tutti i comuni italiani
		r=csv.DictReader(csvfile)
		for row in r or found==1:
			city=row['Nome']
			city=city.lower()
			if city in title:
				print ("trovato: "+city)
				found=1
				coordinate=city
	if key in text or sent==1: #ricerca della parola chiave nel testo e salvataggio nel database
		if date=="":
			date=(time.strftime("%Y-%m-%d"))
		sent=0
		found=0
		print("\n")
		print(textprint)
		print(article.publish_date)
		conn=psycopg2.connect("dbname='article' user='python' host='localHost' password='news'") #collegamento al databse
		cur=conn.cursor()
		cur.execute('INSERT INTO tab1(date,coord,title,link) VALUES (%s, %s, %s, %s)',(date,coordinate, title, link))
		cur.execute("COMMIT")
		conn.commit()
		conn.close()
	print("------------------------------------------------------------------------------------------------------------------------------------")

