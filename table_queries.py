table = {
    "Xem danh sách các xe khách": "SELECT * FROM XE_KHACH",
    "Xem danh sách các tài xế": "SELECT * FROM TAI_XE",
    "Xem danh sách các tuyến xe": "SELECT * FROM TUYEN_XE",
    "Xem danh sách các chuyến xe": """
        SELECT 
            cx.ma_chuyen, cx.ma_tuyen, cx.bien_so,
            tx_lai.ten AS ten_lai_xe, tx_phu.ten AS ten_phu_xe,
            cx.so_khach, cx.gia_ve, cx.ngay_khoi_hanh
        FROM CHUYEN_XE cx

        LEFT JOIN TAI_XE tx_lai ON cx.cmt_lai_xe = tx_lai.cmt
        LEFT JOIN TAI_XE tx_phu ON cx.cmt_phu_xe = tx_phu.cmt
    """,
    "Xem các hệ số tương ứng với cấp đường" : "SELECT * FROM HE_SO_DO_PHUC_TAP",
}

query = {
    "Xem lương của của từng tài xế": """
        SELECT 
            t.cmt AS 'CMT',
            t.ten AS 'TenNhanVien',
            ROUND(COALESCE(SUM(luong.tien_luong), 0), 0) AS 'TongLuong'
        FROM TAI_XE t
        LEFT JOIN (
            -- Lương khi làm Lái xe (300.000 * hệ số lương)
            SELECT 
                c.cmt_lai_xe  AS cmt,
                300000 * hs.he_so_luong AS tien_luong
            FROM CHUYEN_XE c
            JOIN TUYEN_XE tu ON c.ma_tuyen = tu.ma_tuyen
            JOIN HE_SO_DO_PHUC_TAP hs ON tu.do_phuc_tap = hs.do_phuc_tap
            WHERE c.ngay_khoi_hanh <= CURRENT_DATE()

            
            UNION ALL
            
            -- Lương khi làm Phụ xe (Bằng 50% lương lái xe)
            SELECT 
                c.cmt_phu_xe AS cmt,
                (300000 * hs.he_so_luong) / 2 AS tien_luong
            FROM CHUYEN_XE c
            JOIN TUYEN_XE tu ON c.ma_tuyen = tu.ma_tuyen
            JOIN HE_SO_DO_PHUC_TAP hs ON tu.do_phuc_tap = hs.do_phuc_tap
            WHERE c.ngay_khoi_hanh <= CURRENT_DATE()
        ) luong ON t.cmt = luong.cmt
        GROUP BY t.cmt, t.ten;
    """,
    "Xem doanh thu của từng xe trong khoảng thời gian nhất định": """
        SELECT 
            x.bien_so AS 'BienSo',
            COALESCE(SUM(c.so_khach * c.gia_ve), 0) AS 'TongDoanhThu'
        FROM XE_KHACH x
        LEFT JOIN CHUYEN_XE c ON x.bien_so = c.bien_so 
            AND c.ngay_khoi_hanh BETWEEN %s AND %s
        GROUP BY x.bien_so;
    """,
    "Xem trạng thái bảo dưỡng của xe" : """
        SELECT 
            BienSo,
            NgayBaoDuongCuoi,
            SoNgayLich,
            SoKmQuyDoi,
            SoNgayLamViec,
            NgayBaoDuongTiepTheo,
            CASE
                WHEN SoNgayLamViec > 360 THEN 'Quá hạn'
                WHEN SoNgayLamViec = 360 THEN 'Đến hạn'
                ELSE 'Chưa đến hạn'
            END AS TrangThaiBaoDuong
        FROM (
            SELECT 
                xk.bien_so AS BienSo,
                xk.ngay_bao_duong_cuoi AS NgayBaoDuongCuoi,
                ROUND(COALESCE(SUM(tx.do_dai_km * hs.he_so_duong_kho), 0), 2) AS SoKmQuyDoi,
                DATEDIFF(CURRENT_DATE(), xk.ngay_bao_duong_cuoi) AS SoNgayLich,
                DATEDIFF(CURRENT_DATE(), xk.ngay_bao_duong_cuoi) + ROUND(COALESCE(SUM(tx.do_dai_km * hs.he_so_duong_kho), 0) / 100.0) AS SoNgayLamViec,
                DATE_ADD(
                    xk.ngay_bao_duong_cuoi,
                    INTERVAL ROUND(360 - (COALESCE(SUM(tx.do_dai_km * hs.he_so_duong_kho), 0) / 100.0)) DAY
                ) AS NgayBaoDuongTiepTheo

            FROM XE_KHACH xk
            LEFT JOIN CHUYEN_XE cx ON xk.bien_so = cx.bien_so AND cx.ngay_khoi_hanh >= xk.ngay_bao_duong_cuoi
            LEFT JOIN TUYEN_XE tx ON cx.ma_tuyen = tx.ma_tuyen
            LEFT JOIN HE_SO_DO_PHUC_TAP hs ON tx.do_phuc_tap = hs.do_phuc_tap
            GROUP BY xk.bien_so, xk.ngay_bao_duong_cuoi
        ) AS BangTinhToan;
    """
}