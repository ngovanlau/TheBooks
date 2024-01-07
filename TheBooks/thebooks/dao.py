from thebooks.models import Sach, TheLoai
from thebooks import app


def get_the_loai():
    the_loai = TheLoai.query.filter(TheLoai.active.__eq__(True))

    return the_loai.all()


def get_sach(kw, the_loai_id, page):
    sach = Sach.query

    if kw:
        sach = sach.filter(Sach.ten.__contains__(kw))

    if the_loai_id:
        sach = sach.filter(Sach.the_loai_id.__eq__(the_loai_id))

    if page:
        page =int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size

        return sach.slice(start, start + page_size)

    return sach


def get_tac_gia():
    sach = Sach.query.filter(Sach.id.__eq__(1)).first()

    print(sach.tac_gias)


if __name__ == '__main__':
    with app.app_context():
        get_tac_gia()
