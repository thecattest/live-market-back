from configure_app import *
from parse_items_xml import get_json


api_blueprint = Blueprint("api", __name__,
                          template_folder="templates")


@api_blueprint.route("/api/stream/xml", methods=["POST"])
@login_required
def update_feed():
    if request.method == "POST":
        print(list(request.files.keys()))
        print('file' in request.files)
        file = request.files['file']
        print(dir(file))
        print(file.mimetype)
        if file.mimetype != "text/xml":
            return make_response(jsonify({"status": "wrong file type"}))
        items = get_json(file.read())
        current_user.products = items
        db = db_session.create_session().object_session(current_user)
        db.commit()
    return get_feed()


@api_blueprint.route("/api/stream/xml", methods=["GET"])
def get_feed():
    return make_response(current_user.products if current_user.products else '{}')


@api_blueprint.route("/api/cart/<ids>")
def create_cart(ids):
    base_url = "https://hackathon.oggettoweb.com/checkout/cart/addmultiple/products/{}"
    url = base_url.format(ids)
    return redirect(url)


@api_blueprint.route("/api/stream/get_nickname")
@login_required
def get_twitch():
    current_user.stream_started = True
    db = db_session.create_session().object_session(current_user)
    db.commit()
    return current_user.twitch_nickname


@api_blueprint.route("/api/stream/end")
@login_required
def end_stream():
    if current_user.stream_started:
        current_user.stream_started = False
        db = db_session.create_session().object_session(current_user)
        db.commit()


@api_blueprint.route("/api/stream/get/<login>")
def get_stream(login):
    db = db_session.create_session()
    user = db.query(User).filter(User.login == login).first()
    if user and user.stream_started:
        return make_response(jsonify({"status": "ok",
                                      "twitch_nickname": user.twitch_nickname}))
    return make_response(jsonify({"status": "stream is not started"}))
