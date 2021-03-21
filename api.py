from configure_app import *
from parse_items_xml import get_json


api_blueprint = Blueprint("api", __name__,
                          template_folder="templates")


@api_blueprint.route("/api/stream/xml", methods=["GET", "POST"])
@login_required
def feed():
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
    return make_response(current_user.products)


@api_blueprint.route("/api/cart/<ids>")
def create_cart(ids):
    base_url = "https://hackathon.oggettoweb.com/checkout/cart/addmultiple/products/{}"
    url = base_url.format(ids)
    return redirect(url)
