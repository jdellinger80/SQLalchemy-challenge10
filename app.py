##app.py
from unittest import result
from flask import Flask, jsonify

#bring in imports used in Juypter
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, select

app = Flask (__name__)

# conncted to database
engine = create_engine("sqlite:///hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect = True)

# reference tables
Station = Base.classes.station
Measurement = Base.classes.measurement

#Create session from Python to the DB
session = Session(engine)

# home route
@app.route("/")
def home():
    return(
        f"<center> <h3> Welcome to the Hawaii Climate Analysis Local API! </h3> </center>"
        f"<center> <h4> the following API's are available </h4> </center>"
        f"<center> /api/v1.0/precipitation </center>"
        f"<center> /api/v1.0/stations </center>"
        f"<center> /api/v1.0/tobs </center>"
        f"<center> /api/v1.0/start/end </center>"
        f"<center>  </center>"
        f"<center>  </center>"
        f"<center>  </center>" 
    )

# /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
        #Return the year of precipitation from Jupyter
        year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)

        results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= year_ago).all()

        session.close()
    #dictionary with the date as the key and the precipaitation as the value
        precipitation = {date: prcp for date, prcp in results}  
    #convert the tp a json
        return jsonify(precipitation)

# /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).all()
    session.close()
    
    stationList = list(np.ravel(results))
#json
    return jsonify(stationList)

# /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def temperatures():

    year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)

    #return 
    MostActiveStation = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= year_ago).all()
    session.close()
    
    temperaturesList = list(np.ravel(MostActiveStation))

    return jsonify(temperaturesList)

#/api/v1.0/<start> and /api/v1.0/<start>/<end>
# Input http://localhost:5000/api/v1.0/"DDMMYYY""DDMMYYY"
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):

    #select statment for start and end 
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
   
    if not end: 
        startDate = dt.datetime.strptime(start,"%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        session.close()

        temperaturesList = list(np.ravel(results))

        return jsonify(temperaturesList)

    else:

        startDate = dt.datetime.strptime(start,"%m%d%Y")
        endDate = dt.datetime.strptime(end,"%m%d%Y")

        results = session.query(*selection)\
            .filter(Measurement.date >= startDate)\
            .filter(Measurement.date <= endDate).all()

        session.close()

        temperaturesList = list(np.ravel(results))

        return jsonify(temperaturesList)
