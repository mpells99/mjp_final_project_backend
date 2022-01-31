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


class CalendarInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calDate = db.Column(db.String(25), unique=False)
    calDateOptions = db.Column(db.String(25), unique=False)
    booked = db.Column(db.String(144), unique=False)

    def __init__(self, calDate, calDateOptions, booked):
        self.calDate = calDate
        self.calDateOptions = calDateOptions
        self.booked = booked


class CalendarInfoSchema(ma.Schema):
    class Meta:
        fields = ('calDate', 'calDateOptions', 'booked')


calendarInfo_schema = CalendarInfoSchema()
calendarInfos_schema = CalendarInfoSchema(many=True)

db.create_all()

# Endpoint to create a new calendarInfo


@app.route('/calendarInfo', methods=["POST"])
def add_calendarInfo():
    calDate = request.json['calDate']
    calDateOptions = request.json['calDateOptions']
    booked = request.json['booked']

    new_calendarInfo = CalendarInfo(calDate, calDateOptions, booked)

    db.session.add(new_calendarInfo)
    db.session.commit()

    calendarInfo = CalendarInfo.query.get(new_calendarInfo.id)

    return calendarInfo_schema.jsonify(calendarInfo)


# Endpoint to query all guides
@app.route("/calendars", methods=["GET"])
def get_calendars():
    all_calendars = CalendarInfo.query.all()
    result = calendarInfos_schema.dump(all_calendars)
    return jsonify(result)


# Endpoint for querying a single calendar

@app.route("/calendar/<id>", methods=["GET"])
def get_calendar(id):
    calendar = CalendarInfo.query.get(id)
    return calendarInfo_schema.jsonify(calendar)


@app.route('/query-example', methods=["GET"])
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    return '''<h1>The language value is: {}</h1>'''.format(language)


if __name__ == '__main__':
    app.run(debug=True)
