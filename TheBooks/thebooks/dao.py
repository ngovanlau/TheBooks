import hashlib
import cloudinary.uploader
from thebooks.models import Sach, TheLoai, NguoiDung, KhachHang, UserRole, DonHang, ChiTietDonHang
from thebooks import app, db
from flask_login import current_user


def lay_the_loai():
    the_loai = TheLoai.query.filter(TheLoai.active.__eq__(True))

    return the_loai.all()


def lay_tat_ca_sach():
    return Sach.query.filter(Sach.active.__eq__(True)).all()


def lay_sach_theo_id(id):
    return Sach.query.get(id)


def lay_sach(kw=None, the_loai_id=None, trang=None):
    sach = Sach.query

    if kw:
        sach = sach.filter(Sach.ten.contains(kw))

    if the_loai_id:
        sach = sach.filter(Sach.the_loai_id.__eq__(the_loai_id))

    so_sach = sach.count()

    page_size = app.config['PAGE_SIZE']
    if trang:
        trang = int(trang)
        start = (trang - 1) * page_size
        return {
            'sach': sach.slice(start, start + page_size).all(),
            'so_sach': so_sach
        }
    else:
        return {
            'sach': sach.slice(0, page_size).all(),
            'so_sach': so_sach
        }


def them_nguoi_dung(ten=None,username=None, password=None, sdt=None, email=None, dia_chi=None, role=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    nguoi_dung = NguoiDung(ten=ten, username=username, password=password, sdt=sdt, email=email, dia_chi=dia_chi, role=role)

    db.session.add(nguoi_dung)
    return nguoi_dung


def them_khach_hang(ten=None,username=None, password=None, sdt=None, email=None, dia_chi=None):
    nguoi_dung = them_nguoi_dung(ten, username, password, sdt, email, dia_chi, UserRole.khach_hang)
    khach_hang = KhachHang(nguoi_dung=nguoi_dung)

    db.session.add(khach_hang)
    db.session.commit()


def chung_thuc_nguoi_dung(username=None, password=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return NguoiDung.query.filter(NguoiDung.username.__eq__(username),
                                  NguoiDung.password.__eq__(password)).first()

def lay_nguoi_dung_theo_id(id):
    return NguoiDung.query.get(id)


def them_don_hang(gio_hang=None, khach_hang_id=None, nhan_vien_id=None):
    if gio_hang:
        khach_hang = lay_nguoi_dung_theo_id(khach_hang_id).khach_hang
        nhan_vien = lay_nguoi_dung_theo_id(nhan_vien_id).nhan_vien
        h = DonHang(khach_hang=khach_hang, nhan_vien=nhan_vien)
        db.session.add(h)

        for g in gio_hang.values():
            c = ChiTietDonHang(sach_id=g['id'], so_luong=g['so_luong'], don_hang=h)
            db.session.add(c)

        try:
            db.session.commit()
        except:
            return False
        else:
            return True

    return False


def lay_khach_hang_theo_sdt(sdt=None):
    return NguoiDung.query.filter(NguoiDung.sdt.__eq__(sdt)).first()


if __name__ == '__main__':
    with app.app_context():
        print(chung_thuc_nguoi_dung('12345'))