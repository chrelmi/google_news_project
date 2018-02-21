#!/usr/bin/env python3
import psycopg2
import time
from geopy.geocoders import Nominatim
import folium
import sys
map_osm = folium.Map(location=[41.903853, 12.484492],zoom_start=6,tiles='CartoDB dark_matter')
dataoggi = (time.strftime("%Y-%m-%d"))
conn = None
try: #prlevazione dati dal database
	conn=psycopg2.connect("dbname='article' user='python' host='localHost' password='news'")
	cur = conn.cursor()
	cur.execute("SELECT date,coord, title, link FROM tab1")
	rows = cur.fetchall()
	print("The number of parts: ", cur.rowcount)
	for row in rows:
		#var = row
		#row = str(row)
		co = row[1] #asseganzione
		co = str(co)
		co = co.replace("{","")
		co = co.replace("}","")
		if row[0] == dataoggi and co != "" :
			print("\n")
			print(row)
			#if co != "":
			coordinate=co #ricavo le coordinate tramite GEOPY
			geolocator = Nominatim()
			location = geolocator.geocode(coordinate)
			folium.Marker([location.latitude, location.longitude],popup=row[3]).add_to(map_osm)
			print((location.latitude, location.longitude))
			print("-------------------------------------------------------------------------")
	cur.close()
except (Exception, psycopg2.DatabaseError) as error:
	print(error)
finally:
	if conn is not None:
		conn.close()
map_osm.save('mappa.html')
