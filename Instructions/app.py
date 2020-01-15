import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
session = Session(engine)
    
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )


@app.route("/api/v1.0/precipitation")
def prcp():

    
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    lst = list(np.ravel(results))
    
    def Convert(lst): 
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
        return res_dct 
    
    return Convert(lst)


@app.route("/api/v1.0/stations")
def stat():

    
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    lst = list(np.ravel(results))
   
    
    return jsonify(lst)

@app.route("/api/v1.0/tobs")
def tobs():

    import datetime as dt
    
    last_row = session.query(Measurement).order_by(Measurement.id.desc()).first()
    last_date = dt.date(int(last_row.date[:4]), int(last_row.date[5:7]), int(last_row.date[8:10]))
    query_date = last_date - dt.timedelta(days = 365)

    results = session.query(Station.name, Measurement.date, Measurement.tobs).\
                    filter(Station.station == Measurement.station).\
                    filter(Measurement.date == query_date).all()
    
    return jsonify(results)


@app.route("/api/v1.0/<start>")
def start_date(start):
    
    results =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end_date(start,end):
    
    results =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
