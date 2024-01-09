import hashlib
import cloudinary.uploader
from thebooks.models import Sach, TheLoai, NguoiDung, KhachHang, UserRole
from thebooks import app, db
from flask_login import current_user


def lay_the_loai():
    the_loai = TheLoai.query.filter(TheLoai.active.__eq__(True))

    return the_loai.all()


def lay_sach(kw=None, the_loai_id=None, trang=None):
    sach = Sach.query

    if kw:
        sach = sach.filter(Sach.ten.contains(kw))

    if the_loai_id:
        sach = sach.filter(Sach.the_loai_id.__eq__(the_loai_id))

    page_size = app.config['PAGE_SIZE']
    if trang:
        trang = int(trang)
        start = (trang - 1) * page_size
        return sach.slice(start, start + page_size)
    else:
        return sach.slice(0, page_size)


def dem_sach():
    return Sach.query.count()


def dem_sach_theo_the_loai(the_loai_id):
    return Sach.query.filter(Sach.the_loai_id.__eq__(the_loai_id)).count()


def them_nguoi_dung(ten=None,username=None, password=None, sdt=None, email=None, dia_chi=None, role=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    nguoi_dung = NguoiDung(ten=ten, username=username, password=password, sdt=sdt, email=email, dia_chi=dia_chi, role=role)

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


if __name__ == '__main__':
    with app.app_context():
        print(chung_thuc_nguoi_dung('12345'))