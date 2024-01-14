from thebooks import admin, db, dao, utils
from thebooks.models import Sach, NhaXuatBan, TacGia, TheLoai, QuyDinhNhapSach, HinhAnh, PhieuNhap, ChiTietPhieuNhap, NguoiDung, NhanVien, QuanLy, QuanTriVien, QuanLyKho
from flask import session, redirect
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask_admin import expose, BaseView
from thebooks.models import UserRole


class MyView(ModelView):
    edit_modal = True,
    create_modal = True


class AuthenticatedNhanVien(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.nhan_vien


class AuthenticatedQuanLyKho(MyView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.quan_ly_kho


class AuthenticatedQuanLy(MyView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.quan_ly


class AuthenticatedQuantri(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.quan_tri_vien


class AuthenticatedKhachHang(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.khach_hang


class SachView(AuthenticatedQuanLy):
    column_list = ['id', 'ten', 'gia', 'so_luong', 'the_loai', 'tac_gias', 'nha_xuat_ban']
    form_columns = ['ten', 'gia', 'so_luong', 'the_loai_id', 'tac_gias', 'nha_xuat_ban_id', 'active']


class TheLoaiView(AuthenticatedQuanLy):
    pass


class TacGiaView(AuthenticatedQuanLy):
    pass


class NhaXuatBanView(AuthenticatedQuanLy):
    pass


class TheLoaiView(AuthenticatedQuanLy):
    pass


class HinhAnhView(AuthenticatedQuanLy):
    pass


class QuyDinhNhapSachView(AuthenticatedQuantri):
    column_list = ['so_luong_nhap_toi_thieu', 'so_luong_ton_toi_thieu', 'sach_id']


class ThongKeView(AuthenticatedQuantri):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class BanSachView(AuthenticatedNhanVien):
    @expose('/')
    def index(self):
        return self.render('admin/sell.html', thong_tin_don_hang=utils.cart_info(session.get('don_hang')))


class PhieuNhapView(AuthenticatedQuanLyKho):
    pass


class ChiTietPhieuNhapView(AuthenticatedQuanLyKho):
    pass


class NhanVienView(AuthenticatedQuantri):
    pass


class KhachHangView(AuthenticatedQuantri):
    pass


class QuanLyView(AuthenticatedQuantri):
    pass


class QuanLyKhoView(AuthenticatedQuantri):
    pass


class QuanTriView(AuthenticatedQuantri):
    pass


class NguoiDungView(AuthenticatedQuantri):
    pass


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(SachView(Sach, db.session))
admin.add_view(NhaXuatBanView(NhaXuatBan, db.session))
admin.add_view(TacGiaView(TacGia, db.session))
admin.add_view(TheLoaiView(TheLoai, db.session))
admin.add_view(HinhAnhView(HinhAnh, db.session))
# admin.add_view(QuyDinhNhapSachView(QuyDinhNhapSach, db.session))
admin.add_view(PhieuNhapView(PhieuNhap, db.session))
admin.add_view(ChiTietPhieuNhapView(ChiTietPhieuNhap, db.session))
# admin.add_view(NhanVienView(NhanVien, db.session))
# admin.add_view(QuanLyView(QuanLy, db.session))
# admin.add_view(QuanTriView(QuanTriVien, db.session))
# admin.add_view(QuanLyKhoView(QuanLyKho, db.session))
# admin.add_view(NguoiDungView(NguoiDung, db.session))
admin.add_view(BanSachView(name='Bán sách'))
admin.add_view(ThongKeView(name='Thống kê'))
admin.add_view(LogoutView(name='Logout'))
