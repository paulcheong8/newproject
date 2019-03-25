from flask import Flask, jsonify, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
if __name__ == '__main__':
	app.run(debug=True)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
# app.static_folder = 'static'

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
