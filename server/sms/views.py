from flask import Blueprint, request, jsonify
from server import db
from server.models import Users
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import sqlalchemy
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


sms_bp = Blueprint("sms", __name__)

@sms_bp.route("/reply", methods=['POST'])
def sms_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    body = request.values.get('Body', None)
    number = request.values.get('From', None)
    print(body, number)
    user = None 
    for u in Users.query.all():
        if u.phone_number in number:
            user = u
            break
    if user is None:
        print("User not found!")
        return "user not found!"

    if body.lower().strip() == "stop":
        user.active = False 
        db.session.commit()
        resp.message("Reminders stopped!")
        return "None"
    else:
        print("unrecognized message!")
        return "unrecognized message!"
    return str(resp)



    #CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('ToCountry', 'US'), ('ToState', 'AL'), ('SmsMessageSid', 'SM0e85f49f40fe3b7d21a854641232dd25'), ('NumMedia', '0'), ('ToCity', ''), ('FromZip', '02148'), ('SmsSid', 'SM0e85f49f40fe3b7d21a854641232dd25'), ('FromState', 'MA'), ('SmsStatus', 'received'), ('FromCity', 'MELROSE'), ('Body', 'Hi'), ('FromCountry', 'US'), ('To', '+12058467029'), ('ToZip', ''), ('NumSegments', '1'), ('MessageSid', 'SM0e85f49f40fe3b7d21a854641232dd25'), ('AccountSid', 'AC8f73ee090e440b4d35b1020952e45fed'), ('From', '+16179570655'), ('ApiVersion', '2010-04-01')])])