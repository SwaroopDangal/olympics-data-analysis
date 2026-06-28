import pandas as pd
import streamlit as st
import preprocessor,helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio('Select an option', ['Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis'])



if user_menu == 'Medal Tally':
    st.dataframe(helper.medal_tally(df))