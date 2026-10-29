import streamlit as st

from quanly_chucnang.ql_xe_khach import quan_ly_xe_khach
from quanly_chucnang.ql_tai_xe import quan_ly_tai_xe
from quanly_chucnang.ql_tuyen_xe import quan_ly_tuyen_xe
from quanly_chucnang.ql_chuyen_xe import quan_ly_chuyen_xe
from quanly_chucnang.ql_he_so_duong import quan_ly_he_so_duong


st.title("Quản Lý Dữ Liệu Hệ Thống")

bang_duoc_chon = st.selectbox(
    "Vui lòng chọn danh mục bạn muốn quản lý:",
    ["Quản lý Xe Khách", "Quản lý Tài Xế", "Quản lý Tuyến Xe", "Quản lý Hệ số đường", "Quản lý Chuyến Xe"]
)


if bang_duoc_chon == "Quản lý Xe Khách": quan_ly_xe_khach() 
elif bang_duoc_chon == "Quản lý Tài Xế": quan_ly_tai_xe()  
elif bang_duoc_chon == "Quản lý Tuyến Xe": quan_ly_tuyen_xe() 
elif bang_duoc_chon == "Quản lý Hệ số đường": quan_ly_he_so_duong()
elif bang_duoc_chon == "Quản lý Chuyến Xe": quan_ly_chuyen_xe()