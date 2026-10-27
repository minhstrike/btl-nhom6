import streamlit as st
import time
from db import init_connection

def quan_ly_tai_xe():
    connection = init_connection()
    cursor = connection.cursor(dictionary=True)
    
    st.subheader("Quản Lý Dữ Liệu Tài Xế")
    
    cursor.execute("SELECT * FROM TAI_XE")
    danh_sach_tx = cursor.fetchall()
    
    # Tạo danh sách chuỗi hiển thị cho Dropdown Sửa/Xóa (VD: "001090123456 - Nguyễn Văn An")
    danh_sach_tai_xe = [f"{tx['cmt']} - {tx['ten']}" for tx in danh_sach_tx]
    
    tab_them, tab_sua, tab_xoa = st.tabs(["Thêm Mới", "Cập Nhật", "Xóa"])
    
    with tab_them:
        with st.form("form_them_tx", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                cmt = st.text_input("Số CMT/CCCD *")
                ten = st.text_input("Họ và tên *")
                ngay_sinh = st.date_input("Ngày sinh *")
                dia_chi = st.text_input("Địa chỉ")
            with col2:
                ma_bang = st.text_input("Mã số bằng lái *")
                loai_bang = st.selectbox("Loại bằng lái *", ["D", "D1", "D2"])
                tham_nien = st.number_input("Thâm niên (năm)", min_value=0, step=1)
            
            submitted_them = st.form_submit_button("Lưu Dữ Liệu")
            
            if submitted_them:
                if cmt.strip() == "" or ten.strip() == "" or ma_bang.strip() == "":
                    st.error("Vui lòng điền đầy đủ các trường có dấu (*).")
                else:
                    try:
                        sql = "INSERT INTO TAI_XE (cmt, ten, ma_so_bang_lai, loai_bang_lai, dia_chi, ngay_sinh, tham_nien) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (cmt, ten, ma_bang, loai_bang, dia_chi, ngay_sinh, tham_nien))
                        connection.commit()
                        st.success("Đã thêm tài xế thành công!")
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi: {e}")

    with tab_sua:
        if not danh_sach_tai_xe:
            st.info("Chưa có dữ liệu tài xế để sửa.")
        else:
            tx_chon = st.selectbox("Chọn tài xế cần cập nhật:", danh_sach_tai_xe)
            cmt_cu = tx_chon.split(" - ")[0] 
            
            tt_cu = next(tx for tx in danh_sach_tx if tx['cmt'] == cmt_cu)
            
            with st.form("form_sua_tx"):
                st.write(f"Đang sửa thông tin cho tài xế **{tx_chon}**")

                col1, col2 = st.columns(2)
                with col1:
                    ten_moi = st.text_input("Họ và tên *", value=tt_cu['ten'])
                    ngay_sinh_moi = st.date_input("Ngày sinh *", value=tt_cu['ngay_sinh'])
                    dia_chi_moi = st.text_input("Địa chỉ", value=tt_cu['dia_chi'])
                with col2:
                    ma_bang_moi = st.text_input("Mã số bằng lái *", value=tt_cu['ma_so_bang_lai'])
                    
                    danh_sach_bang = ["D", "D1", "D2"]
                    try:
                        index_bang = danh_sach_bang.index(tt_cu['loai_bang_lai'])
                    except ValueError:
                        index_bang = 0
                    loai_bang_moi = st.selectbox("Loại bằng lái *", danh_sach_bang, index=index_bang)
                    
                    tham_nien_moi = st.number_input("Thâm niên (năm)", min_value=0, value=int(tt_cu['tham_nien']) if tt_cu['tham_nien'] else 0)
                
                submitted_sua = st.form_submit_button("Cập Nhật")
                if submitted_sua:
                    if ten_moi.strip() == "" or ma_bang_moi.strip() == "":
                        st.error("Hãy điền đầy đủ thông tin vào các trường có dấu (*).")
                    else:
                        try:
                            sql = "UPDATE TAI_XE SET ten=%s, ma_so_bang_lai=%s, loai_bang_lai=%s, dia_chi=%s, ngay_sinh=%s, tham_nien=%s WHERE cmt=%s"
                            cursor.execute(sql, (ten_moi, ma_bang_moi, loai_bang_moi, dia_chi_moi, ngay_sinh_moi, tham_nien_moi, cmt_cu))
                            connection.commit()
                            st.success(f"Đã cập nhật tài xế {tx_chon} thành công!")
                            time.sleep(1.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi: {e}")

    with tab_xoa:
        if not danh_sach_tai_xe:
            st.info("Chưa có dữ liệu tài xế để xóa.")
        else:
            tx_xoa = st.selectbox("Chọn tài xế cần XÓA:", danh_sach_tai_xe)
            cmt_xoa = tx_xoa.split(" - ")[0]
            
            st.warning(f"Hành động xóa tài xế {tx_xoa} sẽ không thể hoàn tác được. Tài xế đang trong chuyến xe sẽ không thể bị xóa.")
            if st.button("Xác nhận Xóa", type="primary"):
                try:
                    cursor.execute("DELETE FROM TAI_XE WHERE cmt = %s", (cmt_xoa,))
                    connection.commit()
                    st.success(f"Đã xóa tài xế {tx_xoa} khỏi hệ thống!")
                    time.sleep(1.5)
                    st.rerun()
                except Exception:
                    st.error("Không thể xóa tài xế này vì họ đã được phân công chuyến Xx. Hãy xóa các chuyến xe của tài xế này trước!")