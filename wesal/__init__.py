from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/asl_wesal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '6402f96ddc6753297c5d5348641878a9f89a61719b88ee4ef0b1e63972ed624d'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(hours=2000)


db = SQLAlchemy(app)
migrate = Migrate(app,db)



import wesal.routes 