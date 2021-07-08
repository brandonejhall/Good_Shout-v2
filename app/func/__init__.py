from flask import Blueprint

bp = Blueprint('func', __name__)

from app.func import shout,celery,fixtures_task