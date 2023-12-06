# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
import datetime as dt

#Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to the table
measurement = Base.classes.measurement
station = Base.classes.station


# Create an app, being sure to pass __name__
app = Flask(__name__)


# Define what to do when a user hits the index route.
@app.route("/")
def home():
    return (
        f"Welcome to the Home Page! <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )



# Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """This lists all precipitation avaliable from all stations, 
        alongisde the date they were collected"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all Precipitation data for both date and precipitation
    data = session.query(measurement.date, measurement.prcp).all()
    session.close()

    # Create a dictionary from the precipitation data
    precipitation_data = []
    for date, prcp in data:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_data.append(precipitation_dict)
    return jsonify(precipitation_data)



# Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    """This lists all stations names from the dataset"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the entire list of stations from the dataset
    data = session.query(station.station).all()
    session.close()

     # Convert list of tuples into normal list
    all_stations = list(np.ravel(data))

    return jsonify(all_stations)



# Define what to do when a user hits the /temperature route
@app.route("/api/v1.0/tobs")
def temperature():
    """This lists the previous year's temperature data for the 
        most active station: USC00519281"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database for USC00519281 station
    active_station_recent_date = dt.datetime(2017, 8, 18)

    # Calculate the date one year from the last date in data set.
    active_station_one_year_ago = active_station_recent_date - dt.timedelta(days=366)

    # Query the last 12 months of temperature observation data for this station 
    last_year_temp = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= active_station_one_year_ago)

    session.close()

    # Create a dictionary from the precipitation data
    temperature_data = []
    for date, tobs in last_year_temp:
        temperature_dict = {}
        temperature_dict[date] = tobs
        temperature_data.append(temperature_dict)

    return jsonify(temperature_data)



# Define what to do when a user wants temperature data for a specified start date
@app.route("/api/v1.0/<start>")
def start(start):
    """Provides the max, min and average temperatures from dates greater than
        and equal to the start date """
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the temperature data for dates beginning from the start date, calculate the min, max and average temperature
    temp_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start)

    session.close()

    # Create a dictionary from the temperature data
    temperature_data = []
    for min, max, avg in temp_data:
        temperature_dict = {}
        temperature_dict["min"] = min
        temperature_dict["max"] = max
        temperature_dict["average"] = avg
        temperature_data.append(temperature_dict)

    return jsonify(temperature_data)

# Define what to do when a user wants temperature data for a specified start and end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the temperature data for dates between start and end date
    temp_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start, measurement.date <= end)

    session.close()

    # Create a dictionary from the temperature data
    temperature_data = []
    for min, max, avg in temp_data:
        temperature_dict = {}
        temperature_dict["min"] = min
        temperature_dict["max"] = max
        temperature_dict["average"] = avg
        temperature_data.append(temperature_dict)

    return jsonify(temperature_data)

if __name__ == "__main__":
    app.run(debug=True)
