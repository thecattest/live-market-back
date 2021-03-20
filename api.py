from configure_app import *


api_blueprint = Blueprint("api", __name__,
                          template_folder="templates")


@api_blueprint.route("/api/get_stream")
@login_required
def get_stream():
    if current_user.stream:
        return make_response(jsonify(current_user.stream.dict()))
    else:
        return make_response(jsonify({"status": "stream not found"}))


@api_blueprint.route("/api/create_stream/<title>")
@login_required
def create_stream(title):
    if current_user.stream is None:
        db = db_session.create_session()
        db = db.object_session(current_user)
        stream = Stream()
        stream.title = title
        stream.owner = current_user
        db.add(stream)
        db.commit()
        return make_response(jsonify(stream.dict()))
    else:
        return redirect("/api/get_stream")


@api_blueprint.route("/api/end_stream")
@login_required
def end_stream():
    if current_user.stream is not None:
        db = db_session.create_session()
        db = db.object_session(current_user.stream)
        db.delete(current_user.stream)
        db.commit()
        return make_response(jsonify({"status": "ok"}))
    return make_response(jsonify({"status": "stream not found"}))


@api_blueprint.route("/api/cart/<ids>")
def create_cart(ids):
    base_url = "https://hackathon.oggettoweb.com/checkout/cart/addmultiple/products/{}"
    url = base_url.format(ids)
    return redirect(url)
