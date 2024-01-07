from flask import render_template, request
from thebooks import app, dao
from thebooks.admin import *


@app.route('/')
def index():
    kw = request.args.get('kw')
    the_loai_id = request.args.get('the_loai_id')
    page = request.args.get('page')

    sach = dao.get_sach(kw, the_loai_id, page)
    return render_template('index.html', sach=sach)


@app.context_processor
def common_respones():
    return {
        'the_loai': dao.get_the_loai(),
    }


if __name__ == '__main__':
    app.run(debug=True)