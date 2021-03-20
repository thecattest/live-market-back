from flask import Flask, render_template, send_file, request, redirect, make_response, session, abort, jsonify, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from db_init import *
from api import api_blueprint

import os


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.unauthorized_handler(callback=(lambda: redirect('/login')))
app.config['SECRET_KEY'] = 'somenewsupersecretkeyforlivemarketappyouwillneverguess'


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    db.expire_on_commit = False
    return db.query(User).get(user_id)


def main():
    app.register_blueprint(api_blueprint)

    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    # from waitress import serve
    # serve(app, host=host, port=port)
    app.run(host=host, port=port)


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


def send_html(name):
    content = get_file(os.path.join("templates", name))
    return Response(content, mimetype="text/html")


@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return current_user.login
    return "<a href='/login'>log in</a>"


@app.route("/templates/<path:path>")
def send_static(path):
    return send_file(os.path.join(root_dir(), "templates", path))


@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        db = db_session.create_session()
        user = db.query(User).filter(User.login == request.form["login"].strip().lower()).first()
        print(user)
        print(list(request.form.keys()))
        if user and user.check_password(request.form["password"].strip()):
            print(user)
            login_user(user, remember=request.form.get("remember-me", False))
            print("authed")
            return redirect("/")
        return f'{request.form["login"]} {request.form["password"]}'
    return send_html("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
