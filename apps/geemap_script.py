#!/usr/bin/env python
# coding: utf-8

# In[1]:

import ee
import streamlit as st
from streamlit_folium import folium_static
import geemap.eefolium as geemap
import geopandas as gpd

# os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"]
def app():
    st.title("Chlorophyll-a")
    "#streamlit geemap klorofil-a"

    st.markdown("""
    
    Aplikasi Web ini dibuat dengan menggunakan Streamlit untuk menampilkan nilai 
    estimasi besar klorofil-a pada Danau Matano dan Danau Towuti menggunakan 
    algoritma Jaelani 2015 berdasarkan jurnal [Pemetaan Distribusi Spasial Konsentrasi Klorofil-A dengan Landsat 8 di Danau Matano dan Danau Towuti, Sulawesi Selatan](http://lipi.go.id/publikasi/pemetaan-distribusi-spasial-konsentrasi-klorofil-a-dengan-landsat-8-di-danau-matano-dan-danau-towuti-sulawesi-selatan/2062)
    
    """)
    
    with st.echo():
      Map = geemap.Map()

      L8filter = ee.ImageCollection("LANDSAT/LC08/C01/T2_SR") \
              .filterDate("2016-01-01","2020-12-31") \
              .filterMetadata("CLOUD_COVER","less_than",100) \
              .filterBounds(batas) \
              .mean()
              
      #Masking dengan menggunakan polygon batas perairan
      datamask = ee.Image.constant(1).mask()
      
      #Masking dengan data Landsat 8 untuk menghilangkan area yang tidak memiliki nilai dengan melihat salah satu nilai band
      datamask2 = L8filter.expression('b4>=0?1:0',{'b4':L8filter.select('B4')}).eq(1)

      #masking citra Landsat 8
      L8selection = L8filter.divide(10000).divide(3.141593).updateMask(datamask).updateMask(datamask2)

      #--------------------------------------------#
      #           MENGHITUNG KLOROFIL-A            #
      #--------------------------------------------#
      #Computing Chlorophyll-a with Mr. Jaelani's Algoritma
      Chla = L8selection.expression(
        'exp(-0.9889*(log(RrsB4)/log(RrsB5))+0.3619)',{
            'RrsB4': L8selection.select('B4'),
            'RrsB5': L8selection.select('B5')}) \
            .rename('chlor_a').clip(batas)

      print(Chla, 'Clorophil-a')
# Map.addLayer(Chla,{min:-1, max:1, palette: [
#   '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
#   '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
#   '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
#   'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
#   'ff0000', 'de0101', 'c21301', 'a71001', '911003'
#   ]},'Klorofil-a')
      Map.addLayer(Chla,imageVisParam,'Klorofil-a')
      Map

    # call to render Folium map in Streamlit
    folium_static(Map)


# In[ ]:




