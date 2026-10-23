
import streamlit as st
import mysql.connector
connection = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    port=st.secrets["mysql"]["port"],
    database=st.secrets["mysql"]["database"],
)

table = {
    "Xem danh sách các xe khách": "SELECT * FROM XE_KHACH",
    "Xem danh sách các tài xế": "SELECT * FROM TAI_XE",
    "Xem danh sách các tuyến xe": "SELECT * FROM TUYEN_XE",
    "Xem danh sách các chuyến xe": """
        SELECT 
            cx.ma_so_chuyen_xe, cx.ma_tuyen, cx.bien_so,
            tx_lai.ten AS ten_lai_xe, tx_phu.ten AS ten_phu_xe,
            cx.so_khach, cx.gia_ve, cx.ngay_khoi_hanh
        FROM CHUYEN_XE cx

        LEFT JOIN TAI_XE tx_lai ON cx.cmt_lai_xe = tx_lai.cmt
        LEFT JOIN TAI_XE tx_phu ON cx.cmt_phu_xe = tx_phu.cmt
    """,
    "Xem các hệ số tương ứng với cấp đường" : "SELECT * FROM HE_SO_DO_PHUC_TAP",
}

query = {
    "Xem doanh thu của từng xe": """
            SELECT 
                x.bien_so AS 'BienSo',
                COALESCE(SUM(c.so_khach * c.gia_ve), 0) AS 'TongDoanhThu'
            FROM XE_KHACH x
            LEFT JOIN CHUYEN_XE c ON x.bien_so = c.bien_so 
                AND MONTH(c.ngay_khoi_hanh) = MONTH(CURRENT_DATE()) 
                AND YEAR(c.ngay_khoi_hanh) = YEAR(CURRENT_DATE())
            GROUP BY x.bien_so;
        """,
}

selected_table = st.selectbox("Chọn bảng cần xem", list(table))
selected_query = st.selectbox("Chọn truy vấn cần xem", list(query))

try:
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(table[selected_table])
        table_rows = cursor.fetchall()

        cursor.execute(query[selected_query])
        query_rows = cursor.fetchall()
    finally:
        cursor.close()
finally:
    connection.close()

st.title(selected_table)
if table_rows: st.dataframe( table_rows, use_container_width=True)
else: st.info("Bảng không có dữ liệu.")

st.title(selected_query)
if query_rows: st.dataframe( query_rows, use_container_width=True)
else: st.info("Truy vấn không có dữ liệu.")

