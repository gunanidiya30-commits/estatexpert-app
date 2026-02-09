from flask import Blueprint, request, redirect, url_for, session, abort,render_template
from backend.services.property_service import (
    create_property,
    update_property,
    publish_property
)

property_bp = Blueprint(
    "property",
    __name__,
    url_prefix="/properties"
)


def seller_required():
    if not session.get("user_id") or session.get("role") != "seller":
        abort(403)


@property_bp.route("/create", methods=["POST"])
def create():
    seller_required()

    data = {
        "title": request.form["title"],
        "description": request.form.get("description"),
        "property_type": request.form["property_type"],
        "bhk": request.form.get("bhk"),
        "area_sqft": request.form.get("area_sqft"),
        "city": request.form.get("city"),
        "locality": request.form.get("locality"),
        "price": request.form["price"]
    }

    create_property(session["user_id"], data)
    return redirect(url_for("core.home"))


@property_bp.route("/<int:property_id>/edit", methods=["POST"])
def edit(property_id):
    seller_required()

    data = {
        "title": request.form["title"],
        "description": request.form.get("description"),
        "bhk": request.form.get("bhk"),
        "area_sqft": request.form.get("area_sqft"),
        "city": request.form.get("city"),
        "locality": request.form.get("locality"),
        "price": request.form["price"]
    }

    update_property(property_id, session["user_id"], data)
    return redirect(url_for("core.home"))


@property_bp.route("/<int:property_id>/publish", methods=["POST"])
def publish(property_id):
    seller_required()

    publish_property(property_id, session["user_id"])
    return redirect(url_for("core.home"))


@property_bp.route("/dashboard")
def dashboard():
    if not session.get("user_id") or session.get("role") != "seller":
        abort(403)

    from backend.config import get_db_connection

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM properties WHERE owner_id = %s",
        (session["user_id"],)
    )
    properties = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("property/dashboard.html", properties=properties)

@property_bp.route("/")
def public_list():
    from backend.config import get_db_connection

    city = request.args.get("city")
    sort = request.args.get("sort")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM properties WHERE status='active'"
    params = []

    if city:
        query += " AND city = %s"
        params.append(city)

    if sort == "price_asc":
        query += " ORDER BY price ASC"
    elif sort == "price_desc":
        query += " ORDER BY price DESC"

    cursor.execute(query, tuple(params))
    properties = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("property/public_list.html", properties=properties)
