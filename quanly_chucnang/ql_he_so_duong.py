import streamlit as st
import time
from db import init_connection

def quan_ly_he_so_duong():
    connection = init_connection()
    cursor = connection.cursor(dictionary=True)
    
    st.subheader("Quản Lý Dữ Liệu Hệ Số Đường")

    cursor.execute("SELECT * FROM HE_SO_DO_PHUC_TAP")
    danh_sach_hs = cursor.fetchall()

    danh_sach_cap_do = [str(hs['do_phuc_tap']) for hs in danh_sach_hs]
    
    if not danh_sach_cap_do:
        st.info("Chưa có dữ liệu hệ số đường để sửa.")
    else:
        hs_chon = st.selectbox("Chọn cấp độ phức tạp cần cập nhật:", danh_sach_cap_do)
        cap_do_cu = int(hs_chon)
        
        tt_cu = next(hs for hs in danh_sach_hs if hs['do_phuc_tap'] == cap_do_cu)
        
        with st.form("form_sua_he_so"):
            st.write(f"Đang sửa thông tin cho **Cấp độ phức tạp {hs_chon}**")

            col1, col2 = st.columns(2)
            with col1:
                he_so_luong_moi = st.number_input("Hệ số lương *", min_value=0.1, value=float(tt_cu['he_so_luong']), step=0.1, format="%.2f")
            with col2:
                he_so_duong_kho_moi = st.number_input("Hệ số đường khó *", min_value=0.1, value=float(tt_cu['he_so_duong_kho']), step=0.1, format="%.2f")
            
            submitted_sua = st.form_submit_button("Cập Nhật")
            if submitted_sua:
                try:
                    sql = "UPDATE HE_SO_DO_PHUC_TAP SET he_so_luong=%s, he_so_duong_kho=%s WHERE do_phuc_tap=%s"
                    cursor.execute(sql, (he_so_luong_moi, he_so_duong_kho_moi, cap_do_cu))
                    connection.commit()
                    
                    st.success(f"Đã cập nhật hệ số cho cấp độ {hs_chon} thành công!")
                    time.sleep(1.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi: {e}")