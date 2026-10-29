table = {
    "Xem danh sách các xe khách": "SELECT * FROM XE_KHACH",
    "Xem danh sách các tài xế": "SELECT * FROM TAI_XE",
    "Xem danh sách các tuyến xe": "SELECT * FROM TUYEN_XE",
    "Xem danh sách các chuyến xe": """
        SELECT 
            cx.ma_so_chuyen_xe, cx.ma_tuyen, cx.bien_so,
            tx_lai.ten AS ten_lai_xe, tx_phu.ten AS ten_phu_xe,
            cx.so_khach, cx.gia_ve, cx.ngay_khoi_hanh
        FROM CHUYEN_XE cx

        LEFT JOIN TAI_XE tx_lai ON cx.cmt_lai_xe = tx_lai.cmt
        LEFT JOIN TAI_XE tx_phu ON cx.cmt_phu_xe = tx_phu.cmt
    """,
    "Xem các hệ số tương ứng với cấp đường" : "SELECT * FROM HE_SO_DO_PHUC_TAP",
}

query = {
    "Xem doanh thu của từng xe": """
            SELECT 
                x.bien_so AS 'BienSo',
                COALESCE(SUM(c.so_khach * c.gia_ve), 0) AS 'TongDoanhThu'
            FROM XE_KHACH x
            LEFT JOIN CHUYEN_XE c ON x.bien_so = c.bien_so 
                AND MONTH(c.ngay_khoi_hanh) = MONTH(CURRENT_DATE()) 
                AND YEAR(c.ngay_khoi_hanh) = YEAR(CURRENT_DATE())
            GROUP BY x.bien_so;
        """,
    "Xem lương của của từng tài xế": """
        SELECT 
            t.cmt AS 'CMT',
            t.ten AS 'TenNhanVien',
            ROUND(COALESCE(SUM(luong.tien_luong), 0), 0) AS 'TongLuongThang'
        FROM TAI_XE t
        LEFT JOIN (
            -- Lương khi làm Lái xe (300.000 * hệ số lương)
            SELECT 
                c.cmt_lai_xe  AS cmt,
                300000 * hs.he_so_luong AS tien_luong
            FROM CHUYEN_XE c
            JOIN TUYEN_XE tu ON c.ma_tuyen = tu.ma_tuyen
            JOIN HE_SO_DO_PHUC_TAP hs ON tu.do_phuc_tap = hs.do_phuc_tap
            WHERE MONTH(c.ngay_khoi_hanh) = MONTH(CURRENT_DATE()) 
            AND YEAR(c.ngay_khoi_hanh) = YEAR(CURRENT_DATE())
            
            UNION ALL
            
            -- Lương khi làm Phụ xe (Bằng 50% lương lái xe)
            SELECT 
                c.cmt_phu_xe AS cmt,
                (300000 * hs.he_so_luong) / 2 AS tien_luong
            FROM CHUYEN_XE c
            JOIN TUYEN_XE tu ON c.ma_tuyen = tu.ma_tuyen
            JOIN HE_SO_DO_PHUC_TAP hs ON tu.do_phuc_tap = hs.do_phuc_tap
            WHERE MONTH(c.ngay_khoi_hanh) = MONTH(CURRENT_DATE()) 
            AND YEAR(c.ngay_khoi_hanh) = YEAR(CURRENT_DATE())
        ) luong ON t.cmt = luong.cmt
        GROUP BY t.cmt, t.ten;
    """
}