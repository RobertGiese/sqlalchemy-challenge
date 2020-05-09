import numpy as np

from datetime import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Stations = Base.classes.station

app = Flask(__name__)

@app.route("/")
def display():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    results = session.query(Measurements.date, Measurements.prcp).all()
    session.close()
    all_dates = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict[date] = prcp
        all_dates.append(measurement_dict)
    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def station_list():
    session = Session(engine)
    results = session.query(Stations.name).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def last_year():
    session = Session(engine)
    last_12_months = '2016-08-23'
    results = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.station == 'USC00519281').\
        filter(Measurements.date >= last_12_months).\
        order_by(Measurements.date).all()
    session.close()
    last_year = list(np.ravel(results))
    return jsonify(last_year)

@app.route("/api/v1.0/<start>")
def since_date(start):
    session = Session(engine)
    results = session.query(func.max(Measurements.tobs), func.avg(Measurements.tobs), func.min(Measurements.tobs)).\
        filter(Measurements.date >= start).all()
    session.close()
    starting_date = list(np.ravel(results))
    return jsonify(starting_date)

@app.route("/api/v1.0/<start>/<end>")
def range_of_dates(start,end):
    session = Session(engine)
    results = session.query(func.max(Measurements.tobs), func.avg(Measurements.tobs), func.min(Measurements.tobs)).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).all()
    session.close()
    date_range = list(np.ravel(results))
    return jsonify(date_range)


if __name__ == "__main__":
    app.run(debug=True)