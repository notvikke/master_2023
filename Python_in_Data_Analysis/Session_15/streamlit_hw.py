import streamlit as st
import plotly.express as px

import json
import zipfile
import geopandas

import numpy as np
import pandas as pd

def read_and_preprocess_data():
    
    with zipfile.ZipFile('uber-data.zip') as zip:
        with zip.open('madrid-barrios-2020-1-All-DatesByHourBucketsAggregate.csv') as csv:
            data = pd.read_csv(csv)
        with zip.open('madrid_barrios.json') as geojson:
            codes = geopandas.read_file(geojson, encoding="utf-8")

    # change data types in codes because they are not the same as in data
    codes['GEOCODIGO'] = codes['GEOCODIGO'].astype(int)
    codes['MOVEMENT_ID'] = codes['MOVEMENT_ID'].astype(int)

    codes["DISPLAY_NAME"] = codes["DISPLAY_NAME"].str.split().str[1:].str.join(" ")

    # Merge the data with the codes (source)
    data = data.merge(codes[["GEOCODIGO","MOVEMENT_ID","DISPLAY_NAME"]], left_on="sourceid", right_on="MOVEMENT_ID", how="left")
    data = data.rename(columns={"GEOCODIGO":"src_neigh_code", "DISPLAY_NAME":"src_neigh_name"}).drop(columns=["MOVEMENT_ID"])

    data = data.merge(codes[["GEOCODIGO","MOVEMENT_ID","DISPLAY_NAME"]], left_on="dstid", right_on="MOVEMENT_ID", how="left")
    data = data.rename(columns={"GEOCODIGO":"dst_neigh_code", "DISPLAY_NAME":"dst_neigh_name"}).drop(columns=["MOVEMENT_ID"])

    # Create a new date column
    data["year"] = "2020"
    data["date"] = pd.to_datetime(data["day"].astype(str)+data["month"].astype(str)+data["year"].astype(str)+":"+data["start_hour"].astype(str), format="%d%m%Y:%H")

    # Create a new day_period column
    data["day_period"] = data.start_hour.astype(str) + "-" + data.end_hour.astype(str)
    data["day_of_week"] = data.date.dt.weekday
    data["day_of_week_str"] = data.date.dt.day_name()

    return data, codes

data, codes = read_and_preprocess_data()

data.sort_values(by='date', inplace = True)
fig = px.line(data[:50000], x='date', y="mean_travel_time")

fig2 = px.bar(data[:50000], x='day_period', y="mean_travel_time")
fig3 = px.bar(data[:50000], x='day_of_week', y="mean_travel_time")


st.title("Session 14 Homework: Streamlit")
st.header("Travel by Time and Day")
st.plotly_chart(fig)
st.text("A view at the average travel time every day and hour of the year")

st.header("Travel by Time Period")
st.plotly_chart(fig2)
st.text("A view at the average travel time every time period")

st.header("Travel by day of the week")
st.plotly_chart(fig3)
st.text("A view at the average travel time every day of the week")


st.sidebar.selectbox("This is a selector for SOURCE", (data["src_neigh_name"]))
st.sidebar.selectbox("This is a selector for DESTINATION", (data["dst_neigh_name"]))
