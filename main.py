
import streamlit as st
import mysql.connector
connection = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    port=st.secrets["mysql"]["port"],
    database=st.secrets["mysql"]["database"],
)

queries = {
    "Xem danh sách các xe khách": "SELECT * FROM XE_KHACH",
    "Xem danh sách các tài xế": "SELECT * FROM TAI_XE",
    "Xem danh sách các tuyến xe": "SELECT * FROM TUYEN_XE",
    "Xem danh sách các chuyến xe": "SELECT * FROM CHUYEN_XE",
    "Xem lương của các tài xế": """
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
selected_query = st.selectbox("Chọn truy vấn cần xem", list(queries))
st.title(selected_query)

try:
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(queries[selected_query])
        rows = cursor.fetchall()
    finally:
        cursor.close()
finally:
    connection.close()

if rows:
    st.dataframe(rows, use_container_width=True)
else:
    st.info("Truy vấn không có dữ liệu.")
    