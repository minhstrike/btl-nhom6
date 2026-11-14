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
col_title, col_btn = st.columns([0.9, 0.1], vertical_alignment="bottom")
with col_title:
    st.title("Dữ liệu nhà Xe N16")

with col_btn:
    if st.button("", icon=":material/refresh:",type="tertiary", width="stretch"):
        st.rerun()

tab_bang, tab_truyvan = st.tabs(["Bảng dữ liệu", "Truy vấn và báo cáo"])

with tab_bang:
    selected_table = st.selectbox("Chọn dữ liệu cần xem", list(table), key="select_table")
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
        if selected_query == "Xem trạng thái bảo dưỡng của xe":
            subtab_tatca, subtab_chuaden, subtab_denhan, subtab_quahan = st.tabs([
                "Tất cả", 
                "Chưa đến hạn", 
                "Đến hạn", 
                "Chưa đến hạn"
            ])
            
            with subtab_tatca:
                st.dataframe(df_query, column_config=date_config, width="stretch")
                
            with subtab_quahan:
                df_quahan = df_query[df_query['TrangThaiBaoDuong'] == 'Quá hạn']
                st.dataframe(df_quahan, column_config=date_config, width="stretch")
                    
            with subtab_denhan:
                df_denhan = df_query[df_query['TrangThaiBaoDuong'] == 'Đến hạn']
                st.dataframe(df_denhan, column_config=date_config, width="stretch")
        
            with subtab_chuaden:
                df_chuaden = df_query[df_query['TrangThaiBaoDuong'] == 'Chưa đến hạn']
                st.dataframe(df_chuaden, column_config=date_config, width="stretch")     
        else:
            st.dataframe(df_query, column_config=date_config, width="stretch")
    else: st.info("Truy vấn không tìm thấy dữ liệu.")
