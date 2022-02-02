from enum import unique
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calDate = db.Column(db.String(40), unique=False)
    # calDateId = db.Column(db.Integer, primary_key=True)
    calDateOptions = db.Column(db.String(25), unique=False)
    booked = db.Column(db.String(144), unique=False)

    def __init__(self, calDate, id, calDateOptions, booked):
        self.calDate = calDate
        self.id = id
        self.calDateOptions = calDateOptions
        self.booked = booked


class CalendarSchema(ma.Schema):
    class Meta:
        fields = ('calDate', 'id', 'calDateOptions', 'booked')


calendarInfo_schema = CalendarSchema()
calendarInfos_schema = CalendarSchema(many=True)

db.create_all()

# Endpoint to create a new calendar


@app.route('/calendar', methods=["POST"])
def add_calendar():
    calDate = request.json['calDate']
    id = request.json['id']
    calDateOptions = request.json['calDateOptions']
    booked = request.json['booked']

    new_calendar = Calendar(calDate, id, calDateOptions, booked)

    db.session.add(new_calendar)
    db.session.commit()

    calendar = Calendar.query.get(new_calendar.id)

    return calendarInfo_schema.jsonify(calendar)


# Endpoint to query all calendars
@app.route("/calendarInfos", methods=["GET"])
def get_calendars():
    all_calendars = Calendar.query.all()
    result = calendarInfos_schema.dump(all_calendars)
    return jsonify(result)


# Endpoint for querying a single calendar

@app.route("/calendarInfo/<id>", methods=["GET"])
def get_calendar(id):
    calendar = Calendar.query.get(id)
    return calendarInfo_schema.jsonify(calendar)


@app.route('/calendarUpdate/<id>', methods=["PUT"])
def calendar_update(id):
    calendar = Calendar.query.get(id)
    id = request.json['id']
    calDate = request.json['calDate']
    calDateOptions = request.json['calDateOptions']
    booked = request.json['booked']

    calendar.id = id
    calendar.calDate = calDate
    calendar.calDateOptions = calDateOptions
    calendar.booked = booked

    db.session.commit()
    return calendarInfo_schema.jsonify(calendar)


if __name__ == '__main__':
    app.run(debug=True)
