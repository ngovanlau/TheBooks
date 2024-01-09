from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)
app.secret_key = '1@##JDO($E(_(*E)(ƯEd90sw8đUIDF*&F$rjWR@$2424DASDQW'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/thebooks?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config["PAGE_SIZE"] = 4

cloudinary.config(cloud_name='dlqybjdte', api_key='129526211846497', api_secret='5dIF5mGFoQmlmI5pYTMnIYjjkqA')

db = SQLAlchemy(app=app)
login_manager = LoginManager(app=app)

admin = Admin(app=app, name='Quản trị TheBooks', template_mode='bootstrap4')