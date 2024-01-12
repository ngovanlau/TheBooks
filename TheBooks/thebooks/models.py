from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from thebooks import db, app
from flask_login import UserMixin
from datetime import datetime
import enum


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)


class TheLoai(BaseModel):
    ten = Column(String(50), nullable=False, unique=True)
    sachs = relationship('Sach', backref='the_loai', lazy=True)

    def __str__(self):
        return self.ten


class NhaXuatBan(BaseModel):
    ten = Column(String(50), nullable=False, unique=True)
    dia_chi = Column(String(200))
    sachs = relationship('Sach', backref='nha_xuat_ban', lazy=True)

    def __str__(self):
        return self.ten


tacgia_sach = db.Table('tacgia_sach',
                       Column('tac_gia_id', Integer, ForeignKey('tac_gia.id'), primary_key=True),
                       Column('sach_id', Integer, ForeignKey('sach.id'), primary_key=True))


class TacGia(BaseModel):
    ten = Column(String(50), nullable=False)

    def __str__(self):
        return self.ten


class Sach(BaseModel):
    ten = Column(String(50), nullable=False, unique=True)
    gia = Column(Float, default=50000)
    so_luong = Column(Integer, default=0)

    the_loai_id = Column(Integer, ForeignKey(TheLoai.id), nullable=False)
    nha_xuat_ban_id = Column(Integer, ForeignKey(NhaXuatBan.id), nullable=False)
    tac_gias = relationship('TacGia', secondary='tacgia_sach', lazy='subquery', backref=backref('sachs', lazy=True))
    phieu_nhaps = relationship('ChiTietPhieuNhap', backref='sach', lazy=True)
    hinh_anhs = relationship('HinhAnh', backref='sach', lazy=True)
    khach_hangs = relationship('DanhGia', backref='sach', lazy=True)
    don_hangs = relationship('ChiTietDonHang', backref='sach', lazy=True)
    quy_dinh_nhap_sach = relationship('QuyDinhNhapSach', backref='sach', uselist=False, lazy=True)

    def __str__(self):
        return self.ten


class HinhAnh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hinh_anh = Column(String(200))
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)


class PhieuNhap(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_nhap = Column(DateTime, default=datetime.now())
    sachs = relationship('ChiTietPhieuNhap', backref='phieu_nhap', lazy=True)
    quan_ly_kho_id = Column(Integer, ForeignKey('quan_ly_kho.id'), nullable=False)


class ChiTietPhieuNhap(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    so_luong = Column(Integer, default=0)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    phieu_nhap_id = Column(Integer, ForeignKey(PhieuNhap.id), nullable=False)


class DanhGia(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    danh_gia = Column(Integer, default=10)
    nhan_xet = Column(String(500))
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    khach_hang_id = Column(Integer, ForeignKey('khach_hang.id'), nullable=False)


class UserRole(enum.Enum):
    quan_tri_vien = 1
    quan_ly = 2
    quan_ly_kho = 3
    nhan_vien = 4
    khach_hang = 5


class NguoiDung(BaseModel, UserMixin):
    ten = Column(String(50), nullable=False)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    email = Column(String(30))
    sdt = Column(String(20))
    dia_chi = Column(String(200))
    role = Column(Enum(UserRole), default=UserRole.khach_hang)
    khach_hang = relationship('KhachHang', uselist=False, backref='nguoi_dung', lazy=True)
    nhan_vien = relationship('NhanVien', uselist=False, backref='nguoi_dung', lazy=True)
    quan_tri_vien = relationship('QuanTriVien', uselist=False, backref='nguoi_dung', lazy=True)
    quan_ly = relationship('QuanLy', uselist=False, backref='nguoi_dung', lazy=True)
    quan_ly_kho = relationship('QuanLyKho', uselist=False, backref='nguoi_dung', lazy=True)

    def __str__(self):
        return self.ten


class KhachHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar = Column(String(200), default='link')
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    # sachs = relationship('DanhGia', backref='khach_hang', lazy=True)
    don_hangs = relationship('DonHang', backref='khach_hang', lazy=True)


class NhanVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    don_hangs = relationship('DonHang', backref='nhan_vien', lazy=True)


class StatusEnum(enum.Enum):
    cho_thanh_toan = 1
    dang_giao = 2
    da_thanh_toan = 3
    da_huy = 4


class DonHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_tao = Column(DateTime, default=datetime.now())
    status = Column(Enum(StatusEnum), default=StatusEnum.cho_thanh_toan)
    ngay_thanh_toan = Column(DateTime)
    ngay_huy = Column(DateTime)
    sachs = relationship('ChiTietDonHang', backref='don_hang', lazy='subquery')
    khach_hang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id))


class ChiTietDonHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    so_luong = Column(Integer, default=1)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    don_hang_id = Column(Integer, ForeignKey(DonHang.id), nullable=False)


class QuanLyKho(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    phieu_nhap = relationship('PhieuNhap', backref='quan_ly_kho', lazy=True)


class QuanLy(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)


class QuanTriVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)


class QuyDinhNhapSach(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    so_luong_nhap_toi_thieu = Column(Integer, default=150)
    so_luong_ton_toi_thieu = Column(Integer, default=300)
    sach_id = Column(Integer, ForeignKey(Sach.id), unique=True, nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        t1 = TheLoai(ten='Công nghệ thông tin')
        t2 = TheLoai(ten='Lịch sử')
        t3 = TheLoai(ten='Văn học')
        db.session.add(t1)
        db.session.add(t2)
        db.session.add(t3)

        tg1 = TacGia(ten='Nguyễn Văn A')
        tg2 = TacGia(ten='Nguyễn Văn B')
        tg3 = TacGia(ten='Nguyễn Văn C')
        db.session.add(tg1)
        db.session.add(tg2)
        db.session.add(tg3)

        n1 = NhaXuatBan(ten='NXB A', dia_chi='Ho Chi Minh')
        n2 = NhaXuatBan(ten='NXB B', dia_chi='Ho Chi Minh')
        n3 = NhaXuatBan(ten='NXB C', dia_chi='Ho Chi Minh')
        db.session.add(n1)
        db.session.add(n2)
        db.session.add(n3)

        s1 = Sach(ten='Java1', the_loai_id=1, nha_xuat_ban_id=1)
        s2 = Sach(ten='Javascript2', the_loai_id=2, nha_xuat_ban_id=2)
        s3 = Sach(ten='Python3', the_loai_id=3, nha_xuat_ban_id=3)
        s4 = Sach(ten='PHP4', the_loai_id=1, nha_xuat_ban_id=2)
        s5 = Sach(ten='Docker5', the_loai_id=1, nha_xuat_ban_id=3)
        s6 = Sach(ten='Java6', the_loai_id=1, nha_xuat_ban_id=1)
        s7 = Sach(ten='Java7', the_loai_id=1, nha_xuat_ban_id=1)
        s8 = Sach(ten='PHP6', the_loai_id=2, nha_xuat_ban_id=1)
        s9 = Sach(ten='Java9', the_loai_id=3, nha_xuat_ban_id=1)
        s10 = Sach(ten='Docker10', the_loai_id=2, nha_xuat_ban_id=2)
        s11 = Sach(ten='Java11', the_loai_id=2, nha_xuat_ban_id=3)
        s12 = Sach(ten='Python12', the_loai_id=3, nha_xuat_ban_id=2)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.add(s4)
        db.session.add(s5)
        db.session.add(s6)
        db.session.add(s7)
        db.session.add(s8)
        db.session.add(s9)
        db.session.add(s10)
        db.session.add(s11)
        db.session.add(s12)

        db.session.commit()