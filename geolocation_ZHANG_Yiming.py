# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 21:23:20 2018

@author: Zhang Yiming
"""
import pandas as pd
import numpy as np
import multiprocessing
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import time
import googlemaps

#This part is the preparation#
geolocator = Nominatim()
gmaps = googlemaps.Client(key='AIzaSyBBppld7spKzBAbC5kMzD12Yd-977qxjY4')

company = pd.read_excel(r'D:\AFPD\Projects\My code\5. Google API geolocation\data\coname_addresses.xlsx')
df_company_address = company['address']
company['lat'] = ['']*1491
company['lng'] = ['']*1491
company['distance'] = ['']*1491
missing_index = []
white_house = (38.8976763, 77.0387185)

#Using Googel API to find data#
for i_google in company.index:
    location = geocode_result = gmaps.geocode(company.loc[i_google]['address'])
    if len(location) is 0:
        missing_index.append(i_google)
    else:
        company.loc[i_google]['lat'] = geocode_result[0]['geometry']['location']['lat']
        company.loc[i_google]['lng'] = geocode_result[0]['geometry']['location']['lng']
        company.loc[i_google]['distance'] = vincenty((company.loc[i_google]['lat'],company.loc[i_google]['lng']), white_house).km
      
#Using Geopy to find data that google cannot find#
for i_geopy in missing_index:
    location = geolocator.geocode(company.loc[i_geopy]['address'])
    try:
        company.loc[i_geopy]['lat'] = location.latitude
        company.loc[i_geopy]['lng'] = location.longitude
        company.loc[i_geopy]['distance'] = vincenty((location.latitude,location.longitude), white_house).km
    except:
        company.loc[i_geopy]['lat'] = 'connot find lat'
        company.loc[i_geopy]['lng'] = 'connot find lng'
        company.loc[i_geopy]['distance'] = 'connot calculate distance'
        
#Save the result#
company.to_excel(r'D:\AFPD\Projects\My code\5. Google API geolocation\data\output.xlsx')

