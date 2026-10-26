import streamlit as st
import mysql.connector

@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        port=st.secrets["mysql"]["port"],
        database=st.secrets["mysql"]["database"],
    )