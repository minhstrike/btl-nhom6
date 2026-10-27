import streamlit as st
import time
from db import init_connection

def quan_ly_xe_khach():
    connection = init_connection()
    cursor = connection.cursor(dictionary=True)
    
    st.subheader("Quản Lý Dữ Liệu Xe Khách")
    cursor.execute("SELECT bien_so, mau_xe, hang_san_xuat, doi_xe, model, so_ghe, ngay_bao_duong_cuoi FROM XE_KHACH")
    danh_sach_xe = cursor.fetchall()
    danh_sach_bien_so = [xe['bien_so'] for xe in danh_sach_xe]
    
    tab_them, tab_sua, tab_xoa = st.tabs(["Thêm Mới", "Cập Nhật", "Xóa"])
    
    with tab_them:
        with st.form("form_them_xe", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                bien_so = st.text_input("Biển số (VD: 12A-345-67) *")
                mau_xe = st.text_input("Màu xe *")
                hang_sx = st.text_input("Hãng sản xuất *")
                doi_xe = st.number_input("Đời xe (Năm) *", min_value=2000, max_value=2030, value=2026)
            with col2:
                model = st.text_input("Model *")
                so_ghe = st.number_input("Số ghế *", min_value=10, value=40)
                ngay_bd = st.date_input("Ngày bảo dưỡng cuối *")
            
            submitted_them = st.form_submit_button("Lưu Dữ Liệu")
            
            if submitted_them:
                if bien_so.strip() == "" or mau_xe.strip() == "" or hang_sx.strip() == "" or model.strip() == "":
                    st.error("Hãy điền đầy đủ thông tin vào các trường có dấu (*).")
                else:
                    try:
                        sql_insert = """
                            INSERT INTO XE_KHACH (bien_so, mau_xe, hang_san_xuat, doi_xe, model, so_ghe, ngay_bao_duong_cuoi)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(sql_insert, (bien_so, mau_xe, hang_sx, doi_xe, model, so_ghe, ngay_bd))
                        connection.commit() 
                        st.success(f"Đã thêm xe {bien_so} thành công!")
                        time.sleep(1.5)
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Lỗi: {e}")

    with tab_sua:
        if not danh_sach_bien_so:
            st.info("Chưa có dữ liệu xe để sửa.")
        else:
            xe_can_sua = st.selectbox("Chọn biển số xe cần cập nhật:", danh_sach_bien_so)
            thong_tin_cu = next(xe for xe in danh_sach_xe if xe['bien_so'] == xe_can_sua)

            with st.form("form_sua_xe"):
                st.write(f"Đang sửa thông tin cho xe **{xe_can_sua}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    mau_xe_moi = st.text_input("Màu xe", value=thong_tin_cu['mau_xe'])
                    hang_sx_moi = st.text_input("Hãng sản xuất", value=thong_tin_cu['hang_san_xuat'])
                    doi_xe_moi = st.number_input("Đời xe (Năm)", min_value=2000, value=int(thong_tin_cu['doi_xe']))
                with col2:
                    model_moi = st.text_input("Model", value=thong_tin_cu['model'])
                    so_ghe_moi = st.number_input("Số ghế", min_value=10, value=thong_tin_cu['so_ghe'])
                    ngay_bd_moi = st.date_input("Ngày bảo dưỡng cuối", value=thong_tin_cu['ngay_bao_duong_cuoi'])
                
                submitted_sua = st.form_submit_button("Cập Nhật")
                if submitted_sua:
                    try:
                        sql_update = """
                            UPDATE XE_KHACH 
                            SET mau_xe=%s, hang_san_xuat=%s, doi_xe=%s, model=%s, so_ghe=%s, ngay_bao_duong_cuoi=%s 
                            WHERE bien_so=%s
                        """
                        cursor.execute(sql_update, (mau_xe_moi, hang_sx_moi, doi_xe_moi, model_moi, so_ghe_moi, ngay_bd_moi, xe_can_sua))
                        connection.commit()
                        st.success(f"Đã cập nhật xe {xe_can_sua} thành công!")
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi: {e}")

    with tab_xoa:
        if not danh_sach_bien_so:
            st.info("Chưa có dữ liệu xe để xóa.")
        else:
            xe_can_xoa = st.selectbox("Chọn biển số xe cần XÓA:", danh_sach_bien_so)
            st.warning(f"Hành động xóa xe {xe_can_xoa} sẽ không thể hoàn tác được. Xe đang trong chuyến xe sẽ không thể bị xóa.")
            
            if st.button("Xác nhận Xóa", type="primary"):
                try:
                    cursor.execute("DELETE FROM XE_KHACH WHERE bien_so = %s", (xe_can_xoa,))
                    connection.commit()
                    st.success(f"Đã xóa xe {xe_can_xoa} khỏi hệ thống!")
                    time.sleep(1.5)
                    st.rerun()
                except Exception as e:
                    st.error("Không thể xóa chiếc xe này vì nó đã được phân công vào chuyến Xe. Hãy xóa các chuyến xe của xe này trước!")