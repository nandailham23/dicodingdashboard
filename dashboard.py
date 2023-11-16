import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_season_df(df): 
    season_df=df.groupby(by="season").agg({"cnt":"sum"}).reset_index()
    season_df.rename(columns={"cnt":"total_user"},inplace=True)
    return season_df

def create_month_df(df):
    month_df = df.resample(rule="M", on="dteday").agg({
    "cnt": "sum"
    })
    month_df.index = month_df.index.strftime('%Y-%m')
    month_df = month_df.reset_index()
    month_df.rename(columns={
    "cnt": "total_user",
    "dteday": "month"
    }, inplace=True)
    return month_df

def create_weekday_df(df):
    weekday_df=df.groupby(by=["weekday"]).agg({"cnt":"sum"}).reset_index()
    weekday_df.rename(columns={"weekday":"day","cnt":"total_user"},inplace=True)
    weekday_df["day"]=weekday_df["day"].replace([0,1,2,3,4,5,6],["Sun","Mon","Tue","Wed","Thu","Fri","Sat"])
    return weekday_df

def create_growth_df(df):
    growth_df=df.groupby(by="yr").agg({
    "cnt":"sum"
    }).reset_index()
    growth_df.rename(columns={"yr":"year","cnt":"total_user"},inplace=True)
    return growth_df

day_clean_df=pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
day_clean_df.sort_values(by="dteday", inplace=True)
 
for column in datetime_columns:
    day_clean_df[column] = pd.to_datetime(day_clean_df[column])

min_date = day_clean_df["dteday"].min() 
max_date = day_clean_df["dteday"].max() 
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_clean_df[(day_clean_df["dteday"] >= str(start_date)) & 
                (day_clean_df["dteday"] <= str(end_date))]

season_df=create_season_df(main_df) 
month_df=create_month_df(main_df) 
weekday_df=create_weekday_df(main_df) 
growth_df=create_growth_df(main_df) 

st.header('Bike Sharing Dashboard :sparkles:') 

tab1, tab2, tab3, tab4 = st.tabs(["Tab 1", "Tab 2", "Tab 3", "Tab 4"])
with tab1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="total_user", 
        x="year",
        data=growth_df,
        ax=ax
    )
    ax.set_title("Total User's Comparison by Year", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        month_df["month"],
        month_df["total_user"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.set_title("Total User Over Months", loc="center", fontsize=35)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
 
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3","#D3D3D3","#90CAF9","#D3D3D3"]
 
    sns.barplot(
        y="total_user", 
        x="day",
        data=weekday_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Total User by Day", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with tab4:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="total_user", 
        x="season",
        data=season_df.sort_values(by="total_user", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Total User by Season", loc="center", fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

