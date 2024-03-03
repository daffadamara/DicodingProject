import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime
import streamlit_antd_components as sac
import streamlit_shadcn_ui as ui

#Dataset
air_quality = pd.read_csv('dashboard/air_quality_merge.csv')
air_quality.rename(columns={
    'wd': 'WIND_DIRECTION',
    'WSPM': 'WIND_SPEED'
    }, inplace=True)

pollutant_mean = pd.read_csv('dashboard/pollutant_mean.csv')
pollutant_mean[['SO2', 'NO2', 'CO', 'O3', 'pollutant_level']] = pollutant_mean[['SO2', 'NO2', 'CO', 'O3', 'pollutant_level']].apply(lambda x: x.round(2))
temp_by_station = pd.read_csv('dashboard/temp.csv')
rain_by_station = pd.read_csv('dashboard/rain.csv')

# Title
st.title("Air Quality Analysis Dashboard")

# Dashboard
st.markdown(
    """
    ## **Introduction**
    This dashboard contains a bunch of analysis result of an air quality dataset provided by Dicoding Academy. 
    The dataset itself includes information about various air pollutants such as SO2, NO2, CO, O3, as well as temperature, pressure, rain, wind direction, and wind speed.
    """
    )


st.markdown(
    """
    ## **Dashboard**
    """
    )

# Tabs
tabs = sac.tabs([
        sac.TabsItem(label='Overview', icon='house-fill'), 
        sac.TabsItem(label='Analytics', icon='bar-chart-fill'), 
        sac.TabsItem(label='Summary', icon='book-fill'),
], index=0, format_func='title', variant='outline', color='pink', use_container_width=True)

if tabs == 'Overview':
    st.markdown(
    """
    ### **Analysis Questions**
    1. Apakah ada korelasi antara berbagai polutan udara (SO2, NO2, CO, O3)?
    2. Bagaimana konsentrasi polutan udara di berbagai lokasi stasiun?
    3. Apakah ada tren atau pola yang terlihat pada tingkat polutan sepanjang tahun?
    4. Pada stasiun mana suhu mencapai derajat terendah dan tertingginya?
    5. Pada stasiun mana curah hujan mencapai volume tertingginya? 
     
    ### **Dataset Overview :bar_chart:**
    """
    )
    column_hide = sac.checkbox(
        items=[
            'SO2',
            'NO2',
            'CO',
            'O3',
            'TEMP',
            'PRES',
            'RAIN',
            'WIND_DIRECTION',
            'WIND_SPEED',
            sac.CheckboxItem('Datetime', disabled=True),
            sac.CheckboxItem('Year', disabled=True)
        ],
        label='Hide columns', description='Use this to hide selected columns', color='pink', index=[9,10]
    )
 
    column_mask = [col not in column_hide for col in air_quality.columns]
    filtered_air_quality = air_quality.loc[:, column_mask]

    ui.table(data=filtered_air_quality.head(5), maxHeight=50)
    col1, col2, col3 = st.columns(3)
    col1.metric("Maximum Temperature (°C)", f'{round(air_quality.TEMP.max(),1)}°C')
    col2.metric("Maximum Rain Volume (mm)", f'{round(air_quality.RAIN.max(),1)}mm')
    col3.metric("Wind Speed (m/s)", f'{round(air_quality.WIND_SPEED.max(),1)}m/s')
    
    st.metric("Pollutant Level (ppm)", f'{round(pollutant_mean.pollutant_level.max(),1)} ppm')

elif tabs == 'Analytics':
    segment = sac.segmented(
    items=[
        sac.SegmentedItem(label='Correlation'),
        sac.SegmentedItem(label='Pollutant Level'),
        sac.SegmentedItem(label='Time Series'),
        sac.SegmentedItem(label='Temperature'),
        sac.SegmentedItem(label='Rain Volume'),
    ], description='Choose analysis from below to show', label='Analysis type', format_func='title', align='center', 
    size='sm', radius='sm', color='pink', use_container_width=True, divider=False
    )

    if segment == 'Correlation':
        corrAQ = air_quality.corr(method= 'spearman', numeric_only=True)
        st.table(corrAQ)
        with st.expander('Show explanation', expanded=True):
            st.markdown(
                """
                Terdapat korelasi antara SO2, NO2, CO, dan O3 dimana:
                - SO2 memiliki korelasi yang cukup kuat terhadap NO2 (0,49) dan CO (0,53) dan berkorelasi positif.
                - NO2 memiliki korelasi yang kuat terhadap CO (0,69) dan berkorelasi positif.
                - O3 memiliki korelasi yang cukup kuat terhadap NO2 (-0,46) dan cukup lemah terhadap CO (-0,31) dan berkorelasi negatif.
                - O3 memiliki korelasi yang sangat lemah terhadap SO2 (-0,16) dan berkorelasi negatif.
                """
            )
        with st.expander('Show correlation matrix plot'):
            st.image('dashboard/corr.png')
            st.markdown(
                """
                Legends:
                - SO2: Sulphur Dioxide
                - NO2: Nitrogen Dioxide
                - CO: Carbon Monoxide
                - O3: Ozone
                """
            )
    elif segment == 'Pollutant Level':
        ui.table(pollutant_mean)
        with st.expander('Show explanation', expanded=True):
            st.markdown(
                """
                Dari tabel di atas dapat diketahui bahwa:
                - Rata-rata kadar SO2 tertinggi terdapat pada stasiun Nongzhanguan
                - Rata-rata kadar NO2 tertinggi terdapat pada stasiun Wanliu
                - Rata-rata kadar CO tertinggi terdapat pada stasiun Wanshouxigong
                - Rata-rata kadar O3 tertinggi terdapat pada stasiun Huairou
                """
            )
        with st.expander('Show graph'):
            st.image('dashboard/pollutants.png')
    elif segment == 'Time Series':
        pollutant_means_over_years = air_quality.groupby('Year')[['SO2', 'NO2', 'O3']].mean()
        st.image('dashboard/time series.png')
        with st.expander('Show explanation', expanded=True):
            st.markdown(
                """
                Grafik di atas menunjukkan trend antara SO2, NO2, dan O3 pada tahun 2013-2017. 
                Adapun Berdasarkan grafik di atas, tidak terdapat pola trend musiman yang terjadi disepanjang tahun 2013-2017.
                """
            )
    elif segment == 'Temperature':
        temp_by_station.drop(['MIN.RAIN', 'MAX.RAIN'], axis=1, inplace=True)
        col1, col2 = st.columns([3,1])
        with col1:
            ui.table(temp_by_station)
        with col2:
            st.metric("Maximum Temperature (°C)", f'{round(air_quality.TEMP.max(),1)}°C')
            st.metric("Minimum Temperature (°C)", f'{round(air_quality.TEMP.min(),1)}°C')
        with st.expander('Show explanation', expanded=True):
            st.markdown(
                """
                Dari tabel di atas dapat diketahui bahwa:
                - Suhu tertinggi terjadi pada stasiun Gucheng sedangkan suhu terendah terjadi pada stasiun Wanliu.
                - Suhu terendah terjadi pada stasiun Huairou.
                """
            )
    elif segment == 'Rain Volume':
        col1, col2 = st.columns([3,1])
        with col1:
            ui.table(rain_by_station)
        with col2:
            st.metric("Maximum Rain Volume (mm)", f'{round(air_quality.RAIN.max(),1)}mm')
            st.metric("Average Rain Volume (mm)", f'{round(air_quality.RAIN.mean(),1)}mm')
        with st.expander('Show explanation', expanded=True):
            st.markdown(
                """
                Dari tabel di atas dapat diketahui bahwa:
                - Curah hujan dengan volume tertinggi terdapat pada stasiun Aotizhongxin dan Wanliu.
                - Curah hujan di semua stasiun cenderung kecil dengan volume rata-rata yang seragam.
                """
            )

elif tabs == 'Summary':
    st.markdown(
        """
        ### **Summary :book:**
        Dari analisis data yang telah dilakukan terhadap dataset Air Quality, dapat disimpulkan bahwa:
        1. Terdapat korelasi antara SO2, NO2, CO, dan O3 dimana:
            - SO2 memiliki korelasi yang cukup kuat terhadap NO2 (0,49) dan CO (0,53) dan berkorelasi positif.
            - NO2 memiliki korelasi yang kuat terhadap CO (0,69) dan berkorelasi positif.
            - O3 memiliki korelasi yang cukup kuat terhadap NO2 (-0,46) dan cukup lemah terhadap CO (-0,31) dan berkorelasi negatif.
            - O3 memiliki korelasi yang sangat lemah terhadap SO2 (-0,16) dan berkorelasi negatif.
        2. Konsentrasi polutan udara di Stasiun Wanshouxigong memiliki konsentrasi polusi tertinggi dengan rata-rata polutan sebesar 374,83 dan Stasiun Dingling memiliki konsentrasi polusi terendah dengan rata-rata polutan sebesar 253,19.
        3. Berdasarkan data yang dianalisis tidak terdapat pola tren musiman yang terjadi disepanjang tahun sampai tahun 2017.
        4. Suhu tertinggi terjadi pada stasiun Gucheng sedangkan suhu terendah terjadi pada stasiun Wanliu.
        5. Curah hujan dengan volume tertinggi terdapat pada stasiun Aotizhongxin dan Wanliu.
        
        **Disclaimer:**
        *This dashboard is part of Dicoding Academy's project data analysis submission.*
        """
    )

st.caption('*Dashboard created with streamlit :sparkles:*')
