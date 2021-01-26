from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
import numpy as np
import pandas as pd
import datetime as dt

engine=create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect db
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect=True)

#Save references
measurement = Base.classes.measurement
station = Base.classes.station

app=Flask(__name__)

@app.route('/')
def welcome():
    return (
        f"Welcome to the Surfs Up API:<br/>"
        f"Available Routes:<br/>"
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/stations<br/>')

@app.route("/api/v1.0/precipitation")
def prcp():
    session=Session(engine)

#Query for the info
    info = session.query(measurement.date, measurement.prcp).order_by(measurement.date).all()

#Save it as a dictionary
    prcp_date=[]

    for date,prcp in info:
        new_dict = {}
        new_dict[date]=prcp
        prcp_date.append(new_dict)

    session.close()

    return jsonify(prcp_date)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = {}

    #Query for stations
    station_info = session.query(station.station, station.name).all()
    for s,name in station_info:
        stations[s] = name

    session.close()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    tobs_info=session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date > "2016-08-22").all()

    tobs_list = []

    for date, tobs in tobs_info:
        dict = {}
        dict[date] = tobs
        tobs_list.append(dict)
    
    session.close()

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start():
    session =Session(engine)
    
    #Calculate TMIN,TAVG and TMAX with start date
    start = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs))\
    filter(measurement.date >= start).group_by(measurement.date).all()

    session.close()

    start =[]
    for row in start:


@app.route("/api/v1.0/<start>/<end>")
def startend():
    session =Session(engine)

#Calculate TMIN,TAVG and TMAX between dates
info = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs))\
    filter(measurement.date >= start).group_by(measurement.date).all()
    
    session.close()
    
    date = []
    for d in date:


if __name__ == "__main__":
    app.run(debug=True)
 

