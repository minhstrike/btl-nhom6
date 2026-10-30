import streamlit as st
import mysql.connector

@st.cache_resource(ttl=600)
def _create_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        port=st.secrets["mysql"]["port"],
        database=st.secrets["mysql"]["database"],
    )
def init_connection():
    conn = _create_connection()
    try:
        conn.ping(reconnect=True, attempts=3, delay=1)
    except mysql.connector.Error:
        st.cache_resource.clear()
        conn = _create_connection()
    return conn