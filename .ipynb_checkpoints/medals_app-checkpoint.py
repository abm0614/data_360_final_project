import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import re 

st.set_page_config(page_title="Olympic Medal Recipients", layout="wide")

st.title('Olympic Medal Recipients')
st.write("This is an app built from data scraped from Wikipedia" )

data = pd.read_csv('project_data_final.csv')

data = data.dropna()

col1, col2= st.columns([0.5,.4])
with col1:
    prep_time = st.slider(
     "Select a range of prep times in minutes", 0, 60, (10, 30))
data['Prep Time Int'] = pd.to_numeric(data['Prep Time'].str.extract('(\d+)')[0])
mask = (data['Prep Time Int'] >= prep_time[0]) & (data['Prep Time Int'] <= prep_time[1])
filtered_data = data[mask]
with col1:
    total_time = st.slider(
     "Select a range of total times in minutes", 0, 720, (10, 120))
mask2 = (data['Total Time (mins)'] >= total_time[0]) & (data['Total Time (mins)'] <= total_time[1])
filtered_data = data[mask2]
with col1:
    calories = st.slider(
     "Select a range of calories", 0, 1300, (100, 600))
mask3 = (data['Calories'] >= calories[0]) & (data['Calories'] <= calories[1])
filtered_data = data[mask3]

filtered_data = filtered_data.drop(['Prep Time Int', 'Prep Time (mins)', 'Total Time (mins)'], axis=1)

with col2:

    plt.figure(figsize=(9, 5))
    plt.hist(filtered_data['Calories'], bins=20)
    plt.title('Distribution of Calories')
    plt.xlabel('Calories')
    st.pyplot(plt)

st.dataframe(filtered_data, hide_index=True, 
         column_config={"URL": st.column_config.LinkColumn(display_text="Link")})
