# Importing dependencies
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify
from datetime import datetime, timedelta
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model and reflect tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def homepage():
    """List all available api routes."""
    return(
        f"Welcome!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"Or search for the min, max, and average temperature for a specific date or date range (format yyyy-mm-dd)<br/>"
        f"Date example: /api/v1.0/2016-08-03<br/>"
        f"Date range example: /api/v1.0/2016-08-03/2017-01-10"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Query for last 12 months of precipitation data
    session = Session(engine)
    year_ago = datetime(2017, 8, 23) - timedelta(days=365)
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).\
                            filter(Measurement.date >= year_ago).\
                            order_by(Measurement.date).all()
    session.close()

    # Convert date and precipitation results to dictionary
    precipitation_data = []
    for date, prcp in precipitation_scores:
        prcp_dict = {date: prcp}
        precipitation_data.append(prcp_dict)

    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    # Query for all stations from dataset
    session = Session(engine)
    stations = session.query(Station.station).distinct().all()
    session.close()

    # Convert results to list
    station_list = [result[0] for result in stations]

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def temperature():
    # Query for date and temperature observations for the most active station for the most recent year
    session = Session(engine)
    year_ago = datetime(2017, 8, 23) - timedelta(days=365)
    results = session.query(Measurement.tobs).\
            filter(Measurement.station =='USC00519281').\
            filter(Measurement.date >= year_ago).all()
    session.close()

    # Convert results to list
    temperatures_list = [temp[0] for temp in results]

    return jsonify(temperatures_list)

@app.route('/api/v1.0/<start>')
def start_temp(start):
    session = Session(engine)

    # Validate start date format
    try:
        valid_start = datetime.strptime(start, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Date format should be YYYY-MM-DD"}), 404
    
    # Query the earliest and latest date in the database to check if the date is in range
    earliest_date = session.query(func.min(Measurement.date)).scalar()
    latest_date = session.query(func.max(Measurement.date)).scalar()
    
    if start < earliest_date or start > latest_date:
        return jsonify({"error": f"Date out of range. Date should be between {earliest_date} and {latest_date}"}), 404
    
    # Query for min, max, and average temp for all dates >= start date
    start_results = session.query(func.min(Measurement.tobs),
                                   func.max(Measurement.tobs),
                                   func.avg(Measurement.tobs)).\
                                   filter(Measurement.date >= start).all()
    session.close()

    # Create dictionary to hold results
    temp_stats = []
    for min, max, avg in start_results:
        temp_dict = {}
        temp_dict["Temp Min"] = min
        temp_dict["Temp Max"] = max
        temp_dict["Temp Avg"] = avg
        temp_stats.append(temp_dict)

    return jsonify(temp_stats)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    session = Session(engine)

    # Validate date formats
    try:
        valid_start = datetime.strptime(start, "%Y-%m-%d")
        valid_end = datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Date format should be YYYY-MM-DD"}), 404

    if valid_start > valid_end:
        return jsonify({"error": "Start date must be before end date"}), 404
    
    # Query earliest and latest date in the database to check if the dates are in range
    earliest_date = session.query(func.min(Measurement.date)).scalar()
    latest_date = session.query(func.max(Measurement.date)).scalar()
    
    if start < earliest_date or end > latest_date:
        return jsonify({"error": f"Dates out of range. Dates should be between {earliest_date} and {latest_date}"}), 404

    # Query for min, max, and average temp for all dates between the specified start and end dates
    start_end_results = session.query(func.min(Measurement.tobs),
                                   func.max(Measurement.tobs),
                                   func.avg(Measurement.tobs)).\
                                   filter(Measurement.date >= start).\
                                   filter(Measurement.date <= end).all()
    session.close

    # Create dictionary to hold results
    temp_stats = []
    for min, max, avg in start_end_results:
        temp_dict = {}
        temp_dict["Temp Min"] = min
        temp_dict["Temp Max"] = max
        temp_dict["Temp Avg"] = avg
        temp_stats.append(temp_dict)

    return jsonify(temp_stats)


if __name__ == '__main__':
    app.run(debug=True)




