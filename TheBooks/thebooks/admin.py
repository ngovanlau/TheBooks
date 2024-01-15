from thebooks import admin, db, dao, utils
from thebooks.models import Sach, TheLoai, KhachHang, QuyDinhNhapSach, PhieuNhap, ChiTietPhieuNhap, NguoiDung, NhanVien, QuanLy, QuanTriVien, QuanLyKho
from flask import session, redirect, request
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


class AuthenticatedQuanTri(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.quan_tri_vien


class AuthenticatedKhachHang(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.khach_hang


class SachView(AuthenticatedQuanLy):
    column_list = ['id', 'ten', 'gia', 'so_luong', 'the_loai', 'tac_gia', 'nxb']
    form_columns = ['ten', 'gia', 'so_luong', 'the_loai_id', 'tac_gia', 'nxb', 'active']


class TheLoaiView(AuthenticatedQuanLy):
    pass


class QuyDinhNhapSachView(AuthenticatedQuanTri):
    column_list = ['so_luong_nhap_toi_thieu', 'so_luong_ton_toi_thieu', 'sach_id']


class ThongKeTheoDoanhThuView(AuthenticatedQuanTri):
    @expose('/')
    def index(self):
        thang = request.args.get('thang')
        nam = request.args.get('nam')
        return self.render('admin/stats-revenuo.html', thong_ke=dao.thong_ke_doanh_thu_theo_thang(thang=thang, nam=nam), nam=nam, thang=thang)


class ThongKeTheoTanSuatView(AuthenticatedQuanTri):
    @expose('/')
    def index(self):
        thang = request.args.get('thang')
        nam = request.args.get('nam')
        return self.render('admin/stats-frequency.html', thong_ke=dao.thong_ke_theo_tan_suat(thang=thang, nam=nam), nam=nam, thang=thang)


class BanSachView(AuthenticatedNhanVien):
    @expose('/')
    def index(self):
        return self.render('admin/sell.html', thong_tin_don_hang=utils.cart_info(session.get('don_hang')))


class PhieuNhapView(AuthenticatedQuanLyKho):
    form_columns = ['ngay_nhap', 'quan_ly_kho_id']
    column_list = ['id', 'ngay_nhap', 'quan_ly_kho.nguoi_dung']


class ChiTietPhieuNhapView(AuthenticatedQuanLyKho):
    column_list = ['sach', 'phieu_nhap', 'so_luong']
    form_columns = ['sach_id', 'phieu_nhap_id', 'so_luong']


class NhanVienView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']


class KhachHangView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']


class QuanLyView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']


class QuanLyKhoView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']


class QuanTriView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']


class KhachHangView(AuthenticatedQuanLy):
    pass


class NguoiDungView(AuthenticatedQuanLy):
    pass


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(SachView(Sach, db.session))
admin.add_view(TheLoaiView(TheLoai, db.session))
# admin.add_view(QuyDinhNhapSachView(QuyDinhNhapSach, db.session))
admin.add_view(PhieuNhapView(PhieuNhap, db.session))
admin.add_view(ChiTietPhieuNhapView(ChiTietPhieuNhap, db.session))
admin.add_view(NhanVienView(NhanVien, db.session))
admin.add_view(QuanLyView(QuanLy, db.session))
admin.add_view(QuanTriView(QuanTriVien, db.session))
admin.add_view(QuanLyKhoView(QuanLyKho, db.session))
admin.add_view(KhachHangView(KhachHang, db.session))
admin.add_view(NguoiDungView(NguoiDung, db.session))
admin.add_view(BanSachView(name='Bán sách'))
admin.add_view(ThongKeTheoDoanhThuView(name='Thống kê theo doanh thu'))
admin.add_view(ThongKeTheoTanSuatView(name='Thống kê theo tần suất'))
admin.add_view(LogoutView(name='Logout'))
