import streamlit as st
import pandas as pd
from table_queries import table, query
from db import init_connection

connection = init_connection()
date_config = {
    "ngay_bao_duong_cuoi": st.column_config.DateColumn(format="DD/MM/YYYY"),
    "ngay_sinh": st.column_config.DateColumn(format="DD/MM/YYYY"),
    "ngay_khoi_hanh": st.column_config.DateColumn(format="DD/MM/YYYY"),
}
st.title("Quản Lý Dữ Liệu Nhà Xe N16")
tab_bang, tab_truyvan = st.tabs(["Bảng dữ liệu", "Truy vấn và báo cáo"])

with tab_bang:
    selected_table = st.selectbox("Chọn bảng cần xem", list(table), key="select_table")
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(table[selected_table])
        table_rows = cursor.fetchall()
    finally:
        cursor.close()

    st.header(selected_table)
    if table_rows: 
        df_table = pd.DataFrame(table_rows)
        st.dataframe(df_table, column_config=date_config, width="stretch")
    else: st.info("Bảng không có dữ liệu.")

with tab_truyvan:
    selected_query = st.selectbox("Chọn truy vấn cần xem", list(query), key="select_query")
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(table[selected_table])
        table_rows = cursor.fetchall()

        cursor.execute(query[selected_query])
        query_rows = cursor.fetchall()
    finally:
        cursor.close()
        
    st.header(selected_query)
    if query_rows: 
        df_query = pd.DataFrame(query_rows)
        st.dataframe(df_query, column_config=date_config, width="stretch")
    else: st.info("Truy vấn không tìm thấy dữ liệu.")
