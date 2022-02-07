from flask import Flask, request, jsonify
from flask_mongoengine import *
from flask_marshmallow import Marshmallow


app = Flask(__name__)
db = MongoEngine(app)
ma = Marshmallow(app)
db.disconnect()
db.connect(host="mongodb://127.0.0.1:27017/capstone-project")


class Calendar(db.DynamicDocument):
    calDateid = db.StringField(max_length=50)
    calDate = db.StringField(max_length=50)
    calDateOptions = db.StringField(max_length=50)
    booked = db.StringField(max_length=50)

    # def __init__(self, calDate, calDateID, calDateOptions, booked):
    #     self.calDate = calDate
    #     self.calDateID = calDateID
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


calendarInfo_schema = CalendarSchema()
calendarInfos_schema = CalendarSchema(many=True)


# db.create()

# create


@app.route('/calendar', methods=["POST"])
def add_calendar():
    calDateID = request.json["calDateID"]
    calDate = request.json['calDate']
    calDateOptions = request.json['calDateOptions']
    booked = request.json['booked']

    new_calendar = Calendar(calDate, calDateID, calDateOptions, booked)

    # db.create(new_calendar)
    new_calendar.save()

    # calendar = Calendar.query.get(new_calendar.id)

    return calendarInfo_schema.jsonify(new_calendar)


if __name__ == '__main__':
    app.run(debug=True)
