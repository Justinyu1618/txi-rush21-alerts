from server.models import Users
from server import app, db, twilio_client
from datetime import datetime, timedelta
from server.sms.msg_templates import *

#TODO: Option for neighboring counties

def send_starter(user):
    msg = STARTER
    send_msg(user, msg)
    print(f"Sent STARTER. User: {user.phone_number}, ID: {message.sid}")
def build_msg(event):
    msg = REMINDER % (event["title"], event["zoom"])
    return msg

def send_msg(user, msg, update_stats=True):
    message = twilio_client.messages \
                    .create(
                         body=msg,
                         from_=app.config["TWILIO_NUMBER"],
                         to=user.phone_number
                     )
    print(f"Sent REMINDER. User: {user.phone_number}, ID: {message.sid}")

STR_FMT = "%Y-%m-%dT%H:%M"
def run_alerts():
    now = datetime.now()
    upcomingEvent = None
    for event in rushEvents:
        start = datetime.strptime(event["start"], STR_FMT)
        if(start > now and (now + timedelta(minutes=21) > start)):
            upcomingEvent = event
            break
    if(upcomingEvent):
        msg = build_msg(upcomingEvent)
        all_users = Users.query.filter_by(active=True).all()
        try:
            for user in all_users:
                send_msg(user, msg)
        except Exception as e:
            print(f"Could not send message to {user.phone_number}!")
            print(f"Error: {e}")
            