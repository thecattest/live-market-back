from configure_app import *


def main():
    app.register_blueprint(api_blueprint)

    port = int(os.environ.get("PORT", 7007))
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


@app.route("/login", methods=["POST"])
def login_page():
    if request.method == "POST":
        db = db_session.create_session()
        user = db.query(User).filter(User.login == request.form["login"].strip().lower()).first()
        if user and user.check_password(request.form["password"].strip()):
            login_user(user, remember=True)
            return redirect("http://92.53.124.98:3000/")
            return make_response(jsonify({"status": "accepted"}))
        return redirect("http://92.53.124.98:3000/login")
        return make_response(jsonify({"status": "not accepted"}))


@app.route("/xml")
@login_required
def xml():
    return send_html("xml.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("http://92.53.124.98:3000/login")


if __name__ == '__main__':
    main()
