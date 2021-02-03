from flask import Blueprint, request, jsonify
from server import db
from flask_sqlalchemy import SQLAlchemy
from server.models import User, user_location_table
# from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
import sqlalchemy
import json
from .utils import process_places, process_settings, unprocess_settings, delete_user
from server.sms import alert

user_bp = Blueprint("user", __name__)


@user_bp.route('/submit', methods=['POST'])
def submit():
    body = request.get_json()
    user = User.query.filter_by(phone_number=body["phone_number"]).first()
    new = False
    if not user:
       user = User()
       new = True

    # Build response object
    response = {
        "success": False,
        "msg": ""
    }

    # Modify places
    new_places = process_places(body["places"])
    print(new_places)
    if not new_places:
        response["msg"] = "Could not find County of one of your addresses!"
        return jsonify(response), 400

    new_body = {}
    new_body["places"] = new_places[0]
    new_body["locations"] = new_places[1]
    new_body["settings"] = process_settings(body["settings"])
    new_body["phone_number"] = body["phone_number"]

    try:
        user.populate(new_body)
        db.session.add(user)
        db.session.commit()
        response["success"] = True
    except Exception as e:
        raise e #print(e)
        response["msg"] = str(e)
        return jsonify(response), 400

    if new:
        msg = alert.build_starter_msg(user)
        alert.send_msg(user, msg)
    return jsonify(response)


@user_bp.route("/get_data", methods=['POST'])
def get_data():
    response = {
        "msg": "",
        "success": False
    }

    number = request.get_json()["number"]
    print(number)
    user = User.query.filter_by(phone_number=number).first()
    if not user:
        response["msg"] = "No matching user found!"
        return jsonify(response), 200

    try:
        data = {}
        data["places"] = user.places
        data["settings"] = unprocess_settings(user.settings)
    except Exception as e:
        print(f"[get_data] FAILED: {e}")
        return jsonify(response), 500

    response["data"] = data 
    response["success"] = True
    return jsonify(response), 200

@user_bp.route("/delete", methods=['POST'])
def delete():
    response = {
        "msg": "",
        "success": False
    }
    try:
        number = request.get_json()["number"]
        user = User.query.filter_by(phone_number=number).first()
        delete_user(user)
    except Exception as e:
        print(f"[user/delete] {e}")
        response['msg'] = str(e)
        return jsonify(response), 500
    response["success"] = True
    return jsonify(response), 200





stats = {"1277": {'Confirmed': '1340', 'Deaths': '17', 'Recovered': '0', 'Active': '0'}, 1: {'Confirmed': '4', 'Deaths': '0', 'Recovered': '0', 'Active': '0'}}

@user_bp.route("/test", methods=['POST'])
def test():
    user = User.query.filter_by(id=6).first()
    user.update_stats(stats)
    db.session.commit()
    return "hi", 200
