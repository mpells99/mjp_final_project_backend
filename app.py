from enum import unique
from unicodedata import name
from flask import Flask, request, jsonify
from flask_mongoengine import *
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = MongoEngine(app)
ma = Marshmallow(app)
db.disconnect()
db.connect(
    host=f'mongodb+srv://{os.environ.get("usrnm")}:{os.environ.get("passwrd")}@mycapstoneproject.zqef0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')


class Calendar(DynamicDocument):
    calDateID = db.IntField(unique=True)
    calDate = db.StringField(max_length=50)
    calDateOptions = db.StringField(max_length=50)
    booked = db.StringField(max_length=50)
    name = db.StringField(max_lenth=50)
    phone = db.StringField(max_lenth=50)
    email = db.StringField(max_lenth=50)
    address = db.StringField(max_lenth=50)

    # def __init__(self, calDate, id, calDateOptions, booked):
    #     self.calDate = calDate
    #     self.id = id
    #     self.calDateOptions = calDateOptions
    #     self.booked = booked

    def __init__(self,
                 calDate,
                 calDateID,
                 calDateOptions,
                 booked,
                 name,
                 phone,
                 email,
                 address) -> None:
        super().__init__()
        self.calDate = calDate
        self.calDateID = calDateID
        self.calDateOptions = calDateOptions
        self.booked = booked
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address


class CalendarSchema(ma.Schema):
    class Meta:
        fields = ('calDate', 'calDateID', 'calDateOptions',
                  'booked', 'name', 'phone', 'email', 'address')


# calendarInfo_schema = CalendarSchema()
# calendarInfos_schema = CalendarSchema(many=True)


# create

@cross_origin()
@app.route('/calendar', methods=["POST"])
def add_calendar():

    calDateID = request.json["calDateID"]
    calDate = request.json['calDate']
    calDateOptions = request.json['calDateOptions']
    booked = request.json['booked']
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    address = request.json['address']
    new_calendar = Calendar(
        calDate, calDateID, calDateOptions, booked, name, email, phone, address)

    new_calendar.save()

    return jsonify(new_calendar)


@app.route('/calendarInfo/<myid>', methods=["GET"])
def get_calendar(myid):
    calendar = Calendar.objects(
        calDateID=myid).as_pymongo().fields(_id=0).first()
    return jsonify(calendar)


@app.route('/calendarDelete/<myid>', methods=["DELETE"])
def delete_calendar(myid):
    calendar = Calendar.objects(calDateID=myid)
    calendar.delete()

    return "Your calendar entry was deleted"


@app.route('/calendarUpdate/<myid>', methods=["PUT"])
def update_calendar(myid):
    calendar = Calendar.objects(
        calDateID=myid).fields(_id=0)
    calendar.update(calDateID=request.json["calDateID"],
                    calDate=request.json['calDate'],
                    calDateOptions=request.json['calDateOptions'],
                    booked=request.json['booked'],
                    name=request.json["name"],
                    email=request.json['email'],
                    phone=request.json['phone'],
                    address=request.json['address'])

    return "Your calendar entry was updated"


if __name__ == '__main__':
    app.run(debug=True)
