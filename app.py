from enum import unique
from flask import Flask, request, jsonify
from flask_mongoengine import *
from flask_marshmallow import Marshmallow
import json


app = Flask(__name__)
db = MongoEngine(app)
ma = Marshmallow(app)
db.disconnect()
db.connect(host="mongodb://127.0.0.1:27017/capstone-project")


class Calendar(DynamicDocument):
    calDateID = db.IntField(unique=True)
    calDate = db.StringField(max_length=50)
    calDateOptions = db.StringField(max_length=50)
    booked = db.StringField(max_length=50)

    # def __init__(self, calDate, id, calDateOptions, booked):
    #     self.calDate = calDate
    #     self.id = id
    #     self.calDateOptions = calDateOptions
    #     self.booked = booked

    def __init__(self, calDate, calDateID, calDateOptions, booked) -> None:
        super().__init__()
        self.calDate = calDate
        self.calDateID = calDateID
        self.calDateOptions = calDateOptions
        self.booked = booked


class CalendarSchema(ma.Schema):
    class Meta:
        fields = ('calDate', 'calDateID', 'calDateOptions', 'booked')


# calendarInfo_schema = CalendarSchema()
# calendarInfos_schema = CalendarSchema(many=True)


# create


@app.route('/calendar', methods=["POST"])
def add_calendar():

    calDateID = request.json["calDateID"]
    calDate = request.json['calDate']
    calDateOptions = request.json['calDateOptions']
    booked = request.json['booked']
    new_calendar = Calendar(calDate, calDateID, calDateOptions, booked)

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
                    booked=request.json['booked'])

    return "Your calendar entry was updated"


if __name__ == '__main__':
    app.run(debug=True)
