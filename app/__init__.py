from flask import Flask
from flask import Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from celery import Celery

app = Flask(__name__)

app.config.from_object(Config)#completes all configurations 

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)



#IMPORTING BLUEPRINTS
from app.auth import bp as authentication
from app.func import bp as functions

#REGISTERING BLUEPRINTS
app.register_blueprint(authentication)
app.register_blueprint(functions)

from app import auth, models, func
    
