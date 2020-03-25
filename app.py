#import python dependencies
import numpy as np

#import SQL Alchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Create engine and other set up tasks to use SQLAlchemy to access the sqlite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#my resulting tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# import Flask
from flask import Flask, jsonify

# Create an app, being sure to pass __name__
app = Flask(__name__)


# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my Surf's up Homepage!</br>"
        f"Available Routes:<br/>"
        f"Here's how to see the precipitation information: /api/v1.0/precipitation</br>"
        f"Here's how to see the station information: /api/v1.0/stations</br>"
        f"Here's how to see the temperature observations: /api/v1.0/tobs</br>"
        f"Enter a start date in this format (yyyy-mm-dd) to get some summary statistics starting from that date: /api/v1.0/yyyy-mm-dd</br>"
        f"Enter a start and end date in this format (yyyy-mm-dd) to get some summary statistics between those two dates: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd</br>"
        )

#Define what to do when a user hits the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and prcp values n"""
    # Query all prcp
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)


    #return the result
    return jsonify(all_prcp)

#Define what to do when a user hits the stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    stationlist = session.query(Station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    all_stations= []
    for station in stationlist:
        station_dict = {}
        station_dict["Station"] = station
        all_stations.append(station_dict)

    #return the result
    return jsonify(all_stations)
   
#Define what to do when a user hits the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and tobs values"""
    #Query the data 
    query = '''
        SELECT
            date as Date,
            tobs as Temp
        FROM
            measurement
        WHERE
            date >= '2016-08-23'
            '''
    ## EXECUTE MAPS TO WITH SESSION AND FETCHALL MAPS TO ALL
    temp_data = engine.execute(query).fetchall()

    session.close()

    # Create a dictionary from the row data and append to a list of temp obs for the past year given the last data point has a date of 8/23/2017
    all_temps= []
    for date, tobs in temp_data:
        temps_dict = {}
        temps_dict["Date"] = date
        temps_dict["Tobs"] = tobs
        all_temps.append(temps_dict)

    #return the result
    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def getstartdate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the data 
    temps_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all temps from a starting date.
    all_tempsstart= []
    for min, avg, max in temps_start:
        temps_s_dict = {}
        temps_s_dict["Min"] = min
        temps_s_dict["Avg"] = avg
        temps_s_dict["Max"] = max
        all_tempsstart.append(temps_s_dict)


    #return the result
    return jsonify(all_tempsstart)

@app.route("/api/v1.0/<start>/<end>")
def getstartend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and prcp values n"""
    #Query the data 
    temps_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all temp stats from a starting date and end date. 
    all_tempsstartend = []
    for min, avg, max in temps_start_end:
        temps_s_e_dict = {}
        temps_s_e_dict["Min"] = min
        temps_s_e_dict["Avg"] = avg
        temps_s_e_dict["Max"] = max
        all_tempsstartend.append(temps_s_e_dict)

    #return the result
    return jsonify(all_tempsstartend)
    
#ending for the app
if __name__ == "__main__":
    app.run(debug=True)