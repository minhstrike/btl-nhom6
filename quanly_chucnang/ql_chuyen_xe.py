import streamlit as st
import time
from db import init_connection

def quan_ly_chuyen_xe():
    connection = init_connection()
    cursor = connection.cursor(dictionary=True)
    
    st.subheader("Quản Lý Dữ Liệu Chuyến Xe")
    
    cursor.execute("SELECT * FROM CHUYEN_XE")
    danh_sach_cx = cursor.fetchall()
    
    cursor.execute("SELECT ma_tuyen, diem_dau, diem_cuoi FROM TUYEN_XE")
    ds_tuyen_raw = cursor.fetchall()
    ds_tuyen = [f"{t['ma_tuyen']} - {t['diem_dau']} đến {t['diem_cuoi']}" for t in ds_tuyen_raw]
    
    cursor.execute("SELECT bien_so, so_ghe FROM XE_KHACH")
    ds_xe_raw = cursor.fetchall()
    ds_xe = [f"{x['bien_so']} ({x['so_ghe']} chỗ)" for x in ds_xe_raw]
    
    cursor.execute("SELECT cmt, ten, loai_bang_lai FROM TAI_XE")
    ds_tx_raw = cursor.fetchall()
    ds_tx = [f"{tx['cmt']} - {tx['ten']} (Bằng {tx['loai_bang_lai']})" for tx in ds_tx_raw]
    
    ds_hien_thi_cx = [f"{cx['ma_so_chuyen_xe']} - Tuyến {cx['ma_tuyen']}, Xe {cx['bien_so']}, Ngày {cx['ngay_khoi_hanh']}" for cx in danh_sach_cx]
    
    if not ds_tuyen or not ds_xe or not ds_tx:
        st.error("Hệ thống đang thiếu dữ liệu Tuyến Xe, Xe Khách hoặc Tài Xế. Vui lòng thêm dữ liệu cho các mục này trước!")
        return

    tab_them, tab_sua, tab_xoa = st.tabs(["Thêm Mới", "Cập Nhật", "Xóa"])
    
    with tab_them:
        with st.form("form_them_cx", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                ma_chuyen = st.text_input("Mã chuyến xe * (VD: CHY1016)")
                tuyen_chon = st.selectbox("Chọn tuyến xe *", ds_tuyen)
                xe_chon = st.selectbox("Chọn xe khách *", ds_xe)
                ngay_kh = st.date_input("Ngày khởi hành *", format="DD/MM/YYYY")
            with col2:
                lai_xe_chon = st.selectbox("Chọn Lái xe (Lái chính) *", ds_tx)
                phu_xe_chon = st.selectbox("Chọn Phụ xe *", ds_tx)
                so_khach = st.number_input("Số lượng khách hiện tại", min_value=0, value=0, step=1)
                gia_ve = st.number_input("Giá vé (VNĐ)", min_value=0, value=150000, step=10000)
            
            submitted_them = st.form_submit_button("Lưu Dữ Liệu")
            
            if submitted_them:
                ma_tuyen_val = tuyen_chon.split(" - ")[0]
                bien_so_val = xe_chon.split(" (")[0]
                lai_xe_val = lai_xe_chon.split(" - ")[0]
                phu_xe_val = phu_xe_chon.split(" - ")[0]
                
                if ma_chuyen.strip() == "":
                    st.error("Vui lòng nhập Mã chuyến xe.")
                elif lai_xe_val == phu_xe_val:
                    st.error("Lỗi: Lái xe và Phụ xe không được là cùng một người!")
                else:
                    try:
                        sql = "INSERT INTO CHUYEN_XE (ma_so_chuyen_xe, ma_tuyen, bien_so, cmt_lai_xe, cmt_phu_xe, so_khach, gia_ve, ngay_khoi_hanh) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (ma_chuyen, ma_tuyen_val, bien_so_val, lai_xe_val, phu_xe_val, so_khach, gia_ve, ngay_kh))
                        connection.commit()
                        st.success("Đã thêm chuyến xe thành công!")
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi: {e}")

    with tab_sua:
        if not ds_hien_thi_cx:
            st.info("Chưa có dữ liệu chuyến xe để sửa.")
        else:
            cx_chon = st.selectbox("Chọn chuyến xe cần cập nhật:", ds_hien_thi_cx)
            ma_cx_cu = cx_chon.split(" - ")[0] 
            
            tt_cu = next(cx for cx in danh_sach_cx if cx['ma_so_chuyen_xe'] == ma_cx_cu)
            
            idx_tuyen = next((i for i, v in enumerate(ds_tuyen) if v.startswith(tt_cu['ma_tuyen'])), 0)
            idx_xe = next((i for i, v in enumerate(ds_xe) if v.startswith(tt_cu['bien_so'])), 0)
            idx_lai_xe = next((i for i, v in enumerate(ds_tx) if v.startswith(tt_cu['cmt_lai_xe'])), 0)
            idx_phu_xe = next((i for i, v in enumerate(ds_tx) if v.startswith(tt_cu['cmt_phu_xe'])), 0)
            
            with st.form("form_sua_cx"):
                st.write(f"Đang sửa thông tin cho chuyến xe **{ma_cx_cu}**")

                col1, col2 = st.columns(2)
                with col1:
                    tuyen_moi = st.selectbox("Chọn tuyến xe *", ds_tuyen, index=idx_tuyen)
                    xe_moi = st.selectbox("Chọn xe khách *", ds_xe, index=idx_xe)
                    ngay_kh_moi = st.date_input("Ngày khởi hành *", value=tt_cu['ngay_khoi_hanh'], format="DD/MM/YYYY")
                with col2:
                    lai_xe_moi = st.selectbox("Chọn Lái xe (Lái chính) *", ds_tx, index=idx_lai_xe)
                    phu_xe_moi = st.selectbox("Chọn Phụ xe *", ds_tx, index=idx_phu_xe)
                    so_khach_moi = st.number_input("Số lượng khách hiện tại", min_value=0, value=int(tt_cu['so_khach']))
                    gia_ve_moi = st.number_input("Giá vé (VNĐ)", min_value=0.0, value=float(tt_cu['gia_ve']), step=10000.0)
                
                submitted_sua = st.form_submit_button("Cập Nhật")
                if submitted_sua:
                    ma_tuyen_val = tuyen_moi.split(" - ")[0]
                    bien_so_val = xe_moi.split(" (")[0]
                    lai_xe_val = lai_xe_moi.split(" - ")[0]
                    phu_xe_val = phu_xe_moi.split(" - ")[0]
                    
                    if lai_xe_val == phu_xe_val:
                        st.error("Lỗi: Lái xe và Phụ xe không được là cùng một người!")
                    else:
                        try:
                            sql = "UPDATE CHUYEN_XE SET ma_tuyen=%s, bien_so=%s, cmt_lai_xe=%s, cmt_phu_xe=%s, so_khach=%s, gia_ve=%s, ngay_khoi_hanh=%s WHERE ma_so_chuyen_xe=%s"
                            cursor.execute(sql, (ma_tuyen_val, bien_so_val, lai_xe_val, phu_xe_val, so_khach_moi, gia_ve_moi, ngay_kh_moi, ma_cx_cu))
                            connection.commit()
                            st.success(f"Đã cập nhật chuyến xe {ma_cx_cu} thành công!")
                            time.sleep(1.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi: {e}")

    with tab_xoa:
        if not ds_hien_thi_cx:
            st.info("Chưa có dữ liệu chuyến xe để xóa.")
        else:
            cx_xoa = st.selectbox("Chọn chuyến xe cần XÓA:", ds_hien_thi_cx)
            ma_xoa = cx_xoa.split(" - ")[0]
            
            st.warning(f"Hành động xóa chuyến xe {cx_xoa} sẽ không thể hoàn tác được.")
            if st.button("Xác nhận Xóa", type="primary"):
                try:
                    cursor.execute("DELETE FROM CHUYEN_XE WHERE ma_so_chuyen_xe = %s", (ma_xoa,))
                    connection.commit()
                    st.success(f"Đã xóa chuyến xe {cx_xoa} khỏi hệ thống!")
                    time.sleep(1.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi hệ thống khi xóa: {e}")