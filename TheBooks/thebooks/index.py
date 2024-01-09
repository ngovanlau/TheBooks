import math

from flask import render_template, request, redirect
from thebooks import app, dao, login_manager
from flask_login import login_user, logout_user
from thebooks.admin import *


@app.route('/')
def index():
    kw = request.args.get('kw')
    the_loai_id = request.args.get('the_loai_id')
    trang = request.args.get('trang')

    sach = dao.lay_sach(kw, the_loai_id, trang)

    if the_loai_id:
        so_trang = math.ceil(dao.dem_sach_theo_the_loai(the_loai_id) / app.config['PAGE_SIZE'])
    else:
        so_trang = math.ceil(dao.dem_sach() / app.config['PAGE_SIZE'])

    return render_template('index.html', sach=sach, so_trang=so_trang)


@app.context_processor
def common_respones():
    return {
        'the_loai': dao.lay_the_loai(),
    }


@app.route('/register', methods=['get', 'post'])
def register():
    error_message = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            try:
                dao.them_khach_hang(ten=request.form.get('hoTen'),
                                    username=request.form.get('username'),
                                    password=request.form.get('password'),
                                    sdt=request.form.get('sdt'),
                                    email=request.form.get('email'),
                                    dia_chi=request.form.get('diaChi'))
            except Exception as ex:
                error_message = str(ex)
            else:
                return redirect('/login')
        else:
            error_message = 'Mật khẩu không khớp'

    return render_template('register.html', error_message=error_message)


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        nguoi_dung = dao.chung_thuc_nguoi_dung(username=username, password=password)
        if nguoi_dung:
            login_user(nguoi_dung)

            next = request.args.get('next')
            if next:
                return redirect(next)

            return redirect('/')

    return render_template('login.html')


@login_manager.user_loader
def load_user(id):
    return dao.lay_nguoi_dung_theo_id(id)


if __name__ == '__main__':
    app.run(debug=True)