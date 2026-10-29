import streamlit as st
from table_queries import table, query
from db import init_connection

connection = init_connection()

tab_bang, tab_truyvan = st.tabs(["Bảng dữ liệu", "Bảng truy vấn"])

with tab_bang:
    selected_table = st.selectbox("Chọn bảng cần xem", list(table))
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(table[selected_table])
        table_rows = cursor.fetchall()
    finally:
        cursor.close()

    st.header(selected_table)
    if table_rows: st.dataframe(table_rows, width="stretch")
    else: st.info("Bảng không có dữ liệu.")

with tab_truyvan:
    selected_query = st.selectbox("Chọn truy vấn cần xem", list(query))
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(table[selected_table])
        table_rows = cursor.fetchall()

        cursor.execute(query[selected_query])
        query_rows = cursor.fetchall()
    finally:
        cursor.close()
        
    st.header(selected_query)
    if query_rows: st.dataframe(query_rows, width="stretch")
    else: st.info("Truy vấn không tìm thấy dữ liệu.")
