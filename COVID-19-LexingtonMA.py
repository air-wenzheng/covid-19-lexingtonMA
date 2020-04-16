# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 16:49:42 2020

@author: Su
"""
import pandas as pd
import numpy as np
import panel as pn
import hvplot.pandas
import holoviews as hv
import datetime as dt
import os.path, time

pn.extension()

Input_csv_flename = "COVID19_Lexington_2020.csv"
#Input_csv_filename = "https://github.com/air-wenzheng/covid-19-lexingtonMA/blob/master/COVID19_Lexington_2020.csv"

tickers = ['Lexington', 'Middlesex', 'Massachusetts']
ticker = pn.widgets.Select(name='Region', options=tickers,value=tickers[0],width=200)

# this creates the date range slider
date_range_slider = pn.widgets.DateRangeSlider(
name='Date Range',
start=dt.datetime(2020, 1, 1), end=dt.datetime(2020, 5, 31),
value=(dt.datetime(2020, 3, 1), dt.datetime(2020, 5, 15)),width=300)

checkbox = pn.widgets.Checkbox(name='Log Scale',width=100)

#semilogy = hv.Scatter(df,['Date','Lexington'], label='Lexington').opts(logy=True)
title = '### COVID-19 in Lexington, MA'

subtitle = 'This dashboard shows COVID-19 confirmed cases in Lexington, Middlesex and Massachusetts. Data sources come from Town of Lexington and Massachusetts COVID-19 Dashboard.'

#footnote = '(Last updated on 4:30pm April 14, 2020)'
os.environ['TZ'] = 'US/Eastern'
modTimesinceEpoc = os.path.getmtime(Input_csv_flename)
modificationTime = dt.datetime.fromtimestamp(modTimesinceEpoc).strftime('%Y-%m-%d %H:%M:%S')

footnote = "last modified: %s in GMT time" % modificationTime

@pn.depends(ticker.param.value, date_range_slider.param.value,checkbox.param.value)
def get_plot(ticker, date_range, log_scale):

     df= pd.read_csv(Input_csv_flename,skiprows=1)
     df['date'] = pd.to_datetime(df['date'])
     print('log scale switch= ', log_scale)
     print('ticker selection = ',ticker)
     # Load and format the data
     # create date filter using values from the range slider
     # store the first and last date range slider value in a var
     start_date = date_range_slider.value[0] 
     end_date = date_range_slider.value[1] 
     # create filter mask for the dataframe
     mask = (df['date'] > start_date) & (df['date'] <= end_date)
     df = df.loc[mask] # filter the dataframe
     # create the Altair chart object
     semilogy1 = hv.Scatter(df,['date',ticker],vdims=['date',ticker]).opts(tools=['hover','crosshair'],logy=log_scale)
#     semilogy2 = hv.Scatter(df,['date','MiddleSex'], label='MiddleSex').opts(logy=log_scale)
#     semilogy3 = hv.Scatter(df,['date','Massachusetts'], label='Massachusetts').opts(logy=log_scale)

     #chart = alt.Chart(df).mark_line().encode(x='date', y='Confirmed Cases', tooltip=alt.Tooltip(['date','price'])).transform_filter(
     # (datum.symbol == ticker) # this ties in the filter 
     semilogy1.opts(logy=log_scale,width=800,height=600,xlabel='Date',ylabel='Confirmed Cases', show_grid=True, size=5, padding=0.1, line_width=5,legend_position='top_left')
     # also show daily increasement
     temp_diff =  np.diff(df[ticker])
     daily_increase = np.append([0],temp_diff)
#     daily_data =pd.DataFrame()
#     daily_data['date'] = df['date']
#     daily_data['di'] = daily_increase
#     table = hv.Table((df['date'], daily_increase), 'date', 'daily_increase')
     df['di']  =  daily_increase
#     barplot = hv.Bars(table).opts(width=800,height=200,xlabel='Date',ylabel='Daily Increase', show_grid=True,color="red")
     barplot = hv.Scatter(df,['date','di'], vdims=['date','di']).opts(tools=['hover','crosshair'],width=800,height=200,xlabel='Date',ylabel='Daily Increment', show_grid=True, size=5, padding=0.1, line_width=5,color="red")
     curveplot = hv.Curve(df,['date','di']).opts(color="green")
     return pn.Column(semilogy1,barplot * curveplot)
 
dashboard = pn.Column(pn.Row(title, subtitle,pn.layout.Spacer(width=10),background="WhiteSmoke"), pn.Row(date_range_slider,checkbox,ticker),get_plot,footnote)

dashboard.servable('COVID-19-LexingtonMA')
    