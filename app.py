# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import re

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

last_twelve_months = '2016-08-23'
#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Hello! This is the Climate Analysis API from Hawaii!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as 2016-08-23)<br/>"
        f"/api/v1.0/start/end (enter as 2016-08-23/2017-08-23)"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    calc_date = dt.date(query_date.year, query_date.month, query_date.day)
    data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= calc_date).order_by(measurement.date).all()
    precipitation_dict = {date: prcp for date, prcp in data}
    return jsonify(precipitation_dict)



@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(station.station, station.name).all()
    stations_list = [{'station': station, 'name': name} for station, name in station_data]
    return jsonify(stations_list)



@app.route("/api/v1.0/tobs")
def tobs():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= query_date).\
        filter(measurement.station == 'USC00519281').\
        order_by(measurement.date).all()
    tobs_data = []
    for date, tobs in results:
        tobs_data.append({"date": date, "tobs": tobs})
    return jsonify(tobs_data)



@app.route("/api/v1.0/<start>")
def temperature_start(start):
    # Convert the start date string to a datetime object
    start_date = dt.datetime.strptime(start, '2016-08-23')

    # Perform a query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()

    # Extract the results and create a dictionary
    temperature_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temperature_data)


# @app.route("/api/v1.0/<start>/<end>")
# def get_temps_start_end(start, end):
#         # Convert the start date string to a datetime object
#     start_date = dt.datetime.strptime(start, '2016-08-23')
#     end_date = dt.datetime.strptime(end, '2017-08-23')

#     # Perform a query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
#     results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#         filter(measurement.date >= start_date).all()
    
#     results_two = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#         filter(measurement.date <= end_date).all()

#     # Extract the results and create a dictionary
#     temperature_data = {
#         "TMIN": results[0][0],
#         "TAVG": results[0][1],
#         "TMAX": results[0][2]
#     }

#     temperatures_data = {
#         "TMIN": results_two[0][0],
#         "TAVG": results_two[0][1],
#         "TMAX": results_two[0][2]
#     }

#     return jsonify(temperature_data, temperatures_data)

@app.route("/api/v1.0/<start>/<end>")
def get_temps_start_end(start, end):
    # Convert the start and end date strings to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    # Perform a query to calculate TMIN, TAVG, and TMAX for dates between the start and end dates
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date.between(start_date, end_date)).all()

    # Extract the results and create a dictionary
    temperature_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temperature_data)



if __name__ == "__main__":
    app.run(debug=True)