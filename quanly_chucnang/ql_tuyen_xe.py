import streamlit as st
import time
from db import init_connection

def quan_ly_tuyen_xe():
    connection = init_connection()
    cursor = connection.cursor(dictionary=True)
    
    st.subheader("Quản Lý Dữ Liệu Tuyến Xe")
    
    # 1. Lấy dữ liệu tuyến xe và hệ số độ phức tạp
    cursor.execute("SELECT * FROM TUYEN_XE")
    danh_sach_tx = cursor.fetchall()
    
    cursor.execute("SELECT do_phuc_tap FROM HE_SO_DO_PHUC_TAP")
    ds_do_phuc_tap = [row['do_phuc_tap'] for row in cursor.fetchall()]
    
    # Tạo danh sách chuỗi hiển thị cho Dropdown Sửa/Xóa (VD: "TUY001 - Hà Nội đến Hải Phòng")
    danh_sach_tuyen_xe = [f"{tx['ma_tuyen']} - {tx['diem_dau']} đến {tx['diem_cuoi']}" for tx in danh_sach_tx]
    
    tab_them, tab_sua, tab_xoa = st.tabs(["Thêm Mới", "Cập Nhật", "Xóa"])
    
    with tab_them:
        with st.form("form_them_tuyen", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                ma_tuyen = st.text_input("Mã tuyến * (VD: TUY007)")
                diem_dau = st.text_input("Điểm đầu *")
                diem_cuoi = st.text_input("Điểm cuối *")
            with col2:
                do_dai = st.number_input("Độ dài (km)", min_value=0.1, value=100.0, step=1.0)
                if ds_do_phuc_tap:
                    do_phuc_tap = st.selectbox("Cấp độ phức tạp *", ds_do_phuc_tap)
                else:
                    st.error("Chưa có dữ liệu hệ số độ phức tạp. Vui lòng thêm vào CSDL trước.")
                    do_phuc_tap = None
            
            submitted_them = st.form_submit_button("Lưu Dữ Liệu")
            
            if submitted_them and do_phuc_tap is not None:
                if ma_tuyen.strip() == "" or diem_dau.strip() == "" or diem_cuoi.strip() == "":
                    st.error("Vui lòng điền đầy đủ các trường có dấu (*).")
                else:
                    try:
                        sql = "INSERT INTO TUYEN_XE (ma_tuyen, diem_dau, diem_cuoi, do_dai_km, do_phuc_tap) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (ma_tuyen, diem_dau, diem_cuoi, do_dai, do_phuc_tap))
                        connection.commit()
                        st.success("Đã thêm tuyến xe thành công!")
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi: {e}")

    with tab_sua:
        if not danh_sach_tuyen_xe:
            st.info("Chưa có dữ liệu tuyến xe để sửa.")
        else:
            tuyen_chon = st.selectbox("Chọn tuyến xe cần cập nhật:", danh_sach_tuyen_xe)
            ma_cu = tuyen_chon.split(" - ")[0] 
            
            tt_cu = next(tx for tx in danh_sach_tx if tx['ma_tuyen'] == ma_cu)
            
            with st.form("form_sua_tuyen"):
                st.write(f"Đang sửa thông tin cho tuyến xe **{tuyen_chon}**")

                col1, col2 = st.columns(2)
                with col1:
                    diem_dau_moi = st.text_input("Điểm đầu *", value=tt_cu['diem_dau'])
                    diem_cuoi_moi = st.text_input("Điểm cuối *", value=tt_cu['diem_cuoi'])
                with col2:
                    do_dai_moi = st.number_input("Độ dài (km)", min_value=0.1, value=float(tt_cu['do_dai_km']))
                    
                    try:
                        index_dp = ds_do_phuc_tap.index(tt_cu['do_phuc_tap'])
                    except ValueError:
                        index_dp = 0
                    do_phuc_tap_moi = st.selectbox("Cấp độ phức tạp *", ds_do_phuc_tap, index=index_dp)
                
                submitted_sua = st.form_submit_button("Cập Nhật")
                if submitted_sua:
                    if diem_dau_moi.strip() == "" or diem_cuoi_moi.strip() == "":
                        st.error("Hãy điền đầy đủ thông tin vào các trường có dấu (*).")
                    else:
                        try:
                            sql = "UPDATE TUYEN_XE SET diem_dau=%s, diem_cuoi=%s, do_dai_km=%s, do_phuc_tap=%s WHERE ma_tuyen=%s"
                            cursor.execute(sql, (diem_dau_moi, diem_cuoi_moi, do_dai_moi, do_phuc_tap_moi, ma_cu))
                            connection.commit()
                            st.success(f"Đã cập nhật tuyến xe {tuyen_chon} thành công!")
                            time.sleep(1.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi: {e}")

    with tab_xoa:
        if not danh_sach_tuyen_xe:
            st.info("Chưa có dữ liệu tuyến xe để xóa.")
        else:
            tuyen_xoa = st.selectbox("Chọn tuyến xe cần XÓA:", danh_sach_tuyen_xe)
            ma_xoa = tuyen_xoa.split(" - ")[0]
            
            st.warning(f"Hành động xóa tuyến xe {tuyen_xoa} sẽ không thể hoàn tác được. Tuyến xe đang có chuyến xe chạy sẽ không thể bị xóa.")
            if st.button("Xác nhận Xóa", type="primary"):
                try:
                    cursor.execute("DELETE FROM TUYEN_XE WHERE ma_tuyen = %s", (ma_xoa,))
                    connection.commit()
                    st.success(f"Đã xóa tuyến xe {tuyen_xoa} khỏi hệ thống!")
                    time.sleep(1.5)
                    st.rerun()
                except Exception:
                    st.error("Không thể xóa tuyến xe này vì đã được phân công chuyến xe. Hãy xóa các chuyến xe của tuyến này trước!")