from thebooks import admin, db, dao
from thebooks.models import Sach, NhaXuatBan, TacGia, TheLoai, QuyDinhNhapSach, HinhAnh, PhieuNhap, ChiTietPhieuNhap, NguoiDung, NhanVien, QuanLy, QuanTriVien, QuanLyKho
from flask_admin.contrib.sqla import ModelView


class MyView(ModelView):
    edit_modal = True,
    create_modal = True


class SachView(MyView):
    column_list = ['id', 'ten', 'gia', 'so_luong', 'the_loai', 'tac_gias', 'nha_xuat_ban']
    form_columns = ['ten', 'gia', 'so_luong', 'the_loai_id', 'tac_gias', 'nha_xuat_ban_id', 'active']


class TheLoaiView(MyView):
    pass

class QuyDinhNhapSachView(MyView):
    column_list = ['so_luong_nhap_toi_thieu', 'so_luong_ton_toi_thieu', 'sach_id']


admin.add_view(SachView(Sach, db.session))
admin.add_view(ModelView(NhaXuatBan, db.session))
admin.add_view(ModelView(TacGia, db.session))
admin.add_view(TheLoaiView(TheLoai, db.session))
admin.add_view(QuyDinhNhapSachView(QuyDinhNhapSach, db.session))
admin.add_view(ModelView(HinhAnh, db.session))
admin.add_view(ModelView(PhieuNhap, db.session))
admin.add_view(ModelView(ChiTietPhieuNhap, db.session))
admin.add_view(ModelView(NhanVien, db.session))
admin.add_view(ModelView(QuanLy, db.session))
admin.add_view(ModelView(QuanTriVien, db.session))
admin.add_view(ModelView(QuanLyKho, db.session))
