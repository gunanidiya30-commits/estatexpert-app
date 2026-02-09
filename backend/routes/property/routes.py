from flask import Blueprint, request, redirect, url_for, session, abort
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
