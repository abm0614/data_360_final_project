import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title="Multi-Olympic Medal Recipients", layout="wide")

st.title('Multiple Olympic Medal Recipients')
st.write("This is an app built from data scraped from [Wikipedia](https://en.wikipedia.org/wiki/List_of_multiple_Olympic_medalists) containing information about athletes who have won six or more Olympic Medals during their sporting career.")

# Load and clean data
data = pd.read_csv('project_data_final.csv')
data = data.dropna()

# Sidebar for filters
st.sidebar.title('Filters')

# Name search
text_search = st.sidebar.text_input("Search an Athlete", value="")
reg_ex = st.sidebar.checkbox('Regular Expression', value=False)

# Sport selection
sport = st.sidebar.selectbox("Choose a sport", np.insert(np.sort(data['Sport'].unique()), 0, "All Sports"))

# Nation selection
nations = st.sidebar.multiselect("Select Nations", options=np.sort(data['Nation'].unique()), default=None)

# Gender selection
st.sidebar.write("Select Gender:")
gender_col1, gender_col2 = st.sidebar.columns(2)
male = gender_col1.checkbox('Male', key='male', value=True)
female = gender_col2.checkbox('Female', key='female', value=True)

# First and Last Medal Year sliders
first_medal = st.sidebar.slider("Year Range for First Medal won by Athlete", data['First Medal Year'].min(), data['First Medal Year'].max(), (data['First Medal Year'].min(), data['First Medal Year'].max()))
last_medal = st.sidebar.slider("Year Range for Last Medal won by Athlete", data['Last Medal Year'].min(), data['Last Medal Year'].max(), (data['Last Medal Year'].min(), data['Last Medal Year'].max()))

# Olympic Games type selection
st.sidebar.write("Select type of Olympic Games:")
games_col1, games_col2 = st.sidebar.columns(2)
summer = games_col1.checkbox('Summer', key='summer', value=True)
winter = games_col2.checkbox('Winter', key='winter', value=True)

# Apply filters to the dataframe
if len(text_search) > 0:
    if reg_ex:
        data = data[data['Athlete'].str.contains(text_search, regex=True)]
    else:
        data = data[data['Athlete'].str.lower().str.contains(text_search.lower(), regex=False)]

if sport != "All Sports":
    data = data[data['Sport'] == sport]

if nations:
    data = data[data['Nation'].isin(nations)]

if not male:
    data = data[data['Gender'] != 'M']
if not female:
    data = data[data['Gender'] != 'F']

data = data[(data['First Medal Year'] >= first_medal[0]) & (data['First Medal Year'] <= first_medal[1])]
data = data[(data['Last Medal Year'] >= last_medal[0]) & (data['Last Medal Year'] <= last_medal[1])]

if not summer:
    data = data[data['Games'] != 'Summer']
if not winter:
    data = data[data['Games'] != 'Winter']


col1, col2 = st.columns([0.85, 0.2])

with col1:
    st.dataframe(data)

with col2:
    # Displaying total medals and athletes statistics
    total_medals = data['Total'].sum()
    total_athletes = data['Athlete'].nunique()
    st.metric("Total Medals", total_medals)
    st.metric("Total Athletes", total_athletes)

    
    # Medal distribution by type for the selected filter
    medal_types = data[['Gold', 'Silver', 'Bronze']].sum()
    plt.figure(figsize=(4, 4))
    medal_types.plot(kind='pie', colors=['#FFD700', '#C0C0C0', '#CD7F32'], autopct='%1.0f%%')
    plt.title('Medal Distribution')
    plt.xlabel('Medal Type')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    st.pyplot(plt)


# Main panel
col1, col2 = st.columns([0.6, 0.4])

with col1:
    
    # Aggregate total medals by country
    medal_count_by_country = data.groupby('Nation')['Total'].sum().reset_index()

    # Create a choropleth map of total medals by country
    fig = px.choropleth(data_frame=medal_count_by_country,
            locations="Nation",
                locationmode='country names',
                    color="Total",
                    color_continuous_scale="Viridis",
                    title="Total Olympic Medals by Country",
                    labels={"Total": "Total Medals"},
                    hover_name="Nation")

    st.plotly_chart(fig, use_container_width=True)

    athletes_by_sport = data.groupby('Sport')['Athlete'].nunique().reset_index()
    plt.figure(figsize=(6, 4))
    sns.barplot(x='Sport', y='Athlete', data=athletes_by_sport, palette='viridis')
    plt.title('Athlete Count by Sport')
    plt.xlabel('Sport', fontsize=14)
    plt.ylabel('Number of Athletes')
    plt.xticks(rotation=90, fontsize=8) 
    st.pyplot(plt)


with col2:

    plt.figure(figsize=(6, 4))
    bins1 = data['First Medal Year'].max()- data['First Medal Year'].min() + 1
    plt.hist(data['First Medal Year'], bins=bins1, color='#fb7171')
    plt.title('Distribution of First Medal Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Athletes')
    plt.xticks(np.arange(1895, 2020, 5))
    plt.xticks(rotation=90)
    st.pyplot(plt)



    medalists_by_year = data.groupby('First Medal Year')['Athlete'].nunique().reset_index()
    medalists_by_year['Cumulative Medalists'] = medalists_by_year['Athlete'].cumsum()

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(x='First Medal Year', y='Cumulative Medalists', data=medalists_by_year, marker='o', ax=ax, palette='viridis')
    ax.set_title('Total Number of Multi-Medalists (6+) Over Time', fontsize=12)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Cumulative Number of Multi-Medalists', fontsize=8)
    ax.grid(True)
    sns.set_palette("viridis")
    st.pyplot(fig)

    