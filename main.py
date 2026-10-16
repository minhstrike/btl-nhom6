
import streamlit as st
import mysql.connector

connection = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    port=st.secrets["mysql"]["port"],
    database=st.secrets["mysql"]["database"],
)

print('connected')