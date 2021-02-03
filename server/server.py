from flask import Blueprint, request, jsonify
from server import db
from server.models import Users
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import json
from flask import Flask, request
from server.sms.alert import send_starter


server_bp = Blueprint("server", __name__)

@server_bp.route("/add", methods=['GET'])
def add_user():
    number = request.args['number']

    existing = Users.query.filter_by(phone_number=number).first()
    if(not existing):
        new_user = Users()
        new_user.populate({},phone_number=number)
        send_starter(new_user)
        db.session.add(new_user)
        db.session.commit()
    elif(not existing.active):
        send_starter(existing)

    return "success", 200

@server_bp.route("/remove", methods=['GET'])
def remove_user():
    number = request.args['number']

    user = Users.query.filter_by(phone_number=number).first()
    if(user):
        db.session.delete(user)
        db.session.commit()
        print("Removed number!")

    return "success", 200

