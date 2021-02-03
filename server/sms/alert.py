from server.models import Users
from server import app, db, twilio_client
from datetime import datetime, timedelta
from server.sms.msg_templates import *
from server.sms.events import rushEvents
from pytz import timezone

#TODO: Option for neighboring counties

def eastern_now():
    now_utc = datetime.now(timezone('UTC'))
    return now_utc.astimezone(timezone("US/Eastern"))

def naive_to_eastern(naive):
    return timezone("US/Eastern").localize(naive)

def send_starter(user):
    msg = STARTER
    send_msg(user, msg)
    print(f"Sent STARTER. User: {user.phone_number}")

def build_msg(event):
    msg = REMINDER % (event["name"], event["zoom"])
    return msg

def send_msg(user, msg, update_stats=True):
    message = twilio_client.messages \
                    .create(
                         body=msg,
                         from_=app.config["TWILIO_NUMBER"],
                         to=user.phone_number
                     )
    print(f"Sent REMINDER. User: {user.phone_number}, ID: {message.sid}")

STR_FMT = "%Y-%m-%dT%H:%M:%S"
def run_alerts():
    now = eastern_now()
    upcomingEvent = None
    for event in rushEvents:
        start = naive_to_eastern(datetime.strptime(event["start"], STR_FMT))
        print(now, start)
        if(start > now and (now + timedelta(minutes=21) > start) and (now + timedelta(minutes=10) < start)):
            upcomingEvent = event
            break
    if(upcomingEvent):
        msg = build_msg(upcomingEvent)
        all_users = Users.query.all()
        try:
            for user in all_users:
                send_msg(user, msg)
        except Exception as e:
            print(f"Could not send message to {user.phone_number}!")
            print(f"Error: {e}")
            