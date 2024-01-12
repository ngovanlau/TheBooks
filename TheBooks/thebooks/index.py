import math

from flask import render_template, request, redirect, session, jsonify
from thebooks import app, dao, login_manager, utils
from flask_login import login_user, logout_user
from thebooks.admin import *


@app.route('/')
def index():
    kw = request.args.get('kw')
    the_loai_id = request.args.get('the_loai_id')
    trang = request.args.get('trang')

    du_lieu = dao.lay_sach(kw, the_loai_id, trang)
    sach = du_lieu['sach']

    so_trang = math.ceil(du_lieu['so_sach'] / app.config['PAGE_SIZE'])

    return render_template('index.html', sach=sach, so_trang=so_trang)


@app.context_processor
def common_respones():
    return {
        'the_loai': dao.lay_the_loai(),
        'thong_tin_gio_hang': utils.cart_info(session.get('gio_hang'))
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/gio_hang')
def cart():
    return render_template('cart.html')


@app.route('/api/gio_hang', methods=['post'])
def add_to_cart():
    data = request.json

    gio_hang = session.get('gio_hang')
    if gio_hang is None:
        gio_hang = {}

    id = str(data.get('id'))
    if id in gio_hang:
        gio_hang[id]['so_luong'] += 1
    else:
        gio_hang[id] = {
            'id': id,
            'ten': data.get('ten'),
            'gia': data.get('gia'),
            'so_luong': 1
        }

    session['gio_hang'] = gio_hang

    return jsonify(utils.cart_info(gio_hang))


@app.route('/api/gio_hang/<sach_id>', methods=['put'])
def update_cart(sach_id):
    gio_hang = session.get('gio_hang')

    if gio_hang and sach_id in gio_hang:
        so_luong = request.json.get('so_luong')
        gio_hang[sach_id]['so_luong'] = int(so_luong)

    session['gio_hang'] = gio_hang
    return jsonify(utils.cart_info(gio_hang))


@app.route('/api/gio_hang/<sach_id>', methods=['delete'])
def delete_cart(sach_id):
    gio_hang = session.get('gio_hang')

    if gio_hang and sach_id in gio_hang:
        del gio_hang[sach_id]

    session['gio_hang'] = gio_hang
    return jsonify(utils.cart_info(gio_hang))


@app.route('/api/pay', methods=['post'])
def pay():
    gio_hang = session.get('gio_hang')
    if dao.them_don_hang(gio_hang):
        del session['gio_hang']
        return jsonify({'status': 200})

    return jsonify({'status': 500, 'error_message': 'Something wrong!'})


if __name__ == '__main__':
    app.run(debug=True)