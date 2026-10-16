
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
        WITH LuongVaiTroLaiXe AS (
            SELECT
                cx.LaiXe_CMT AS CMT,
                SUM(
                    100000 * CASE tx.CapPhucTap
                        WHEN 1 THEN 1.0
                        WHEN 2 THEN 1.25
                        WHEN 3 THEN 1.5
                    END * 2
                ) AS LuongLaiXe
            FROM CHUYEN_XE cx
            JOIN TUYEN_XE tx ON cx.MaTuyen = tx.MaTuyen
            WHERE MONTH(cx.NgayChay) = MONTH(CURDATE())
                AND YEAR(cx.NgayChay) = YEAR(CURDATE())
            GROUP BY cx.LaiXe_CMT
        ),
        LuongVaiTroPhuXe AS (
            SELECT
                cx.PhuXe_CMT AS CMT,
                SUM(
                    100000 * CASE tx.CapPhucTap
                        WHEN 1 THEN 1.0
                        WHEN 2 THEN 1.25
                        WHEN 3 THEN 1.5
                    END
                ) AS LuongPhuXe
            FROM CHUYEN_XE cx
            JOIN TUYEN_XE tx ON cx.MaTuyen = tx.MaTuyen
            WHERE MONTH(cx.NgayChay) = MONTH(CURDATE())
                AND YEAR(cx.NgayChay) = YEAR(CURDATE())
            GROUP BY cx.PhuXe_CMT
        )
        SELECT
            t.CMT,
            t.Hoten AS TenNhanVien,
            COALESCE(l.LuongLaiXe, 0) + COALESCE(p.LuongPhuXe, 0) AS TongLuongThang
        FROM TAI_XE t
        LEFT JOIN LuongVaiTroLaiXe l ON t.CMT = l.CMT
        LEFT JOIN LuongVaiTroPhuXe p ON t.CMT = p.CMT
        ORDER BY TongLuongThang DESC, TenNhanVien ASC
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
    