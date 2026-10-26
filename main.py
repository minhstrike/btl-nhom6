import streamlit as st

page_1 = st.Page("trang1_xem.py", title="Xem Dữ Liệu", icon="📊", default=True)
page_2 = st.Page("trang2_quan_ly.py", title="Quản Lý Dữ Liệu", icon="✏️")

pg = st.navigation([page_1, page_2])
pg.run()