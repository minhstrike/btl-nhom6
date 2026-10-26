import streamlit as st
from table_queries import table, query
from db import init_connection

connection = init_connection()

col_table, col_query = st.columns(2)
with col_table: selected_table = st.selectbox("Chọn bảng cần xem", list(table))
with col_query: selected_query = st.selectbox("Chọn truy vấn cần xem", list(query))

cursor = connection.cursor(dictionary=True)
try:
    cursor.execute(table[selected_table])
    table_rows = cursor.fetchall()

    cursor.execute(query[selected_query])
    query_rows = cursor.fetchall()
finally:
    cursor.close()


st.title(selected_table)
if table_rows: st.dataframe(table_rows, width="stretch")
else: st.info("Bảng không có dữ liệu.")

st.title(selected_query)
if query_rows: st.dataframe(query_rows, width="stretch")
else: st.info("Truy vấn tìm thấy dữ liệu.")