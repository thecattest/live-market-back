from flask import Flask, render_template, send_file, \
    request, redirect, make_response, session, abort, jsonify, \
    Response, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS

from db_init import *
from api import api_blueprint

import os


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.unauthorized_handler(callback=(lambda: redirect('/login')))
app.config['SECRET_KEY'] = 'somenewsupersecretkeyforlivemarketappyouwillneverguess'
CORS(app)

@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    db.expire_on_commit = False
    return db.query(User).get(user_id)
