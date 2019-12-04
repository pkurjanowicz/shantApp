from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
import datetime
from models import Messages
import os
from db_instance import db
import psycopg2
from models import Messages
import pytz
from pytz import timezone

app = Flask(__name__)

def last_poop_date():
    last_poop_date = Messages.query.filter_by(pooper_name='Shant').all()
    poop_item_list =  [poop_date.poop_date for poop_date in last_poop_date]
    last_poop_date = poop_item_list[-1]
    return last_poop_date

def poop_message():
    poop_messages = Messages.query.filter_by(pooper_name='Shant').all()
    poop_item_list =  [poop_message.poop_message for poop_message in poop_messages]
    last_poop_message = poop_item_list[-1]
    return last_poop_message

def poop_rating():
    poop_ratings = Messages.query.filter_by(pooper_name='Shant').all()
    poop_item_list =  [poop_rating.poop_rating for poop_rating in poop_ratings]
    last_poop_rating = poop_item_list[-1]
    return last_poop_rating

def verify_shant(number):
    if number == '+12032312081' or number == "+18186068167":
        return True
    return False

def update_status():
    date_format='%m-%d-%Y'
    date = datetime.datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    date_today = date.strftime(date_format)
    if date_today != last_poop_date():
        return False
    return True

@app.route('/', methods=['GET'])
def render_app():
    has_shant_pooped = update_status()
    if has_shant_pooped == True:
        return render_template('index.html', message='Yes', last_poop_date=last_poop_date(), poop_message=poop_message(), poop_rating=poop_rating())
    return render_template('index.html', message="No", last_poop_date=last_poop_date(), poop_message=poop_message(), poop_rating=poop_rating())

@app.route("/sms", methods=['GET'])
def sms_ahoy_reply():
    number = request.args.get('From')
    body = request.args.get('Body')
    rating = request.args.get('poop_rating')
    if verify_shant(number):
        date_format='%m-%d-%Y'
        date = datetime.datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        date_today = date.strftime(date_format)
        new_poop = Messages(pooper_name='Shant',poop_date=date_today, poop_message=body, poop_rating=rating)
        db.session.add(new_poop)
        db.session.commit()
        return 'Success'
    return 'Falure'

    """
    RESPONSE DATA EXAMPLE(QUERY STRING)
    ?ToCountry=US
    &ToState=AL
    &SmsMessageSid=SMc5c48883a3902d997b64e39dca6bd5c9
    &NumMedia=0
    &ToCity=TUSCALOOSA
    &FromZip=06484
    &SmsSid=SMc5c48883a3902d997b64e39dca6bd5c9
    &FromState=CT
    &SmsStatus=received
    &FromCity=DERBY
    &Body=hey+there
    &FromCountry=US
    &To=%2B12052933232
    &ToZip=35405
    &NumSegments=1
    &MessageSid=SMc5c48883a3902d997b64e39dca6bd5c9
    &AccountSid=ACd11feb6ef2a175264fd6e40fc62ad19d
    &From=%2B12032312081
    &ApiVersion=2010-04-01
    """

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(user=os.environ["DB_USER"],pw=os.environ["DB_PASS"],url=os.environ["DB_URL"],db=os.environ["DB_NAME"])
with app.app_context():
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)