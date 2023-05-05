import datetime as dt
from pathlib import Path

from flask import Flask, jsonify
from sqlalchemy import create_engine, desc, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


#################################################
# Database Setup
#################################################
db_path = Path(__file__).parent / "Resources/hawaii.sqlite"
# threading error fix: https://stackoverflow.com/questions/48218065/objects-created-in-a-thread-can-only-be-used-in-that-same-thread
engine = create_engine("sqlite:///" + str(db_path),
                       connect_args={'check_same_thread': False})

# reflect the database and tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes["measurement"]
Station = Base.classes["station"]

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#####################################################################
# Create Constants
#####################################################################
def most_active_station() -> str:
    """Gives the most active station from the database
    :return: string station
    """
    active_stations = session.query(Measurement.station,
                                    func.count(Measurement.station).label("count"))\
                             .join(Station, Measurement.station == Station.station)\
                             .group_by(Measurement.station)\
                             .order_by(desc("count"))\
                             .all()
    return active_stations[0].station  # selecting from named tuple


# Constants
MOST_RECENT_DATE = dt.datetime.strptime(session.query(func.max(Measurement.date)).scalar(), r"%Y-%m-%d").date()
ONE_YEAR_PRIOR_DATE = MOST_RECENT_DATE - dt.timedelta(days=365)
MOST_ACTIVE_STATION = most_active_station()


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """Starting page listing all the routes"""
    return"""
          <h1>Welcome</h1>
          <h2>Simple climate app of Hawaii data</h2>
          <h3>Available routes:</h3>
          /api/v1.0/precipitation</br>
          /api/v1.0/stations</br>
          /api/v1.0/tobs</br>
          /api/v1.0/&lt;start&gt;</br>
          /api/v1.0/&lt;start&gt;/&lt;end&gt;
          """


@app.route("/api/v1.0/precipitation")
def precipitation():
    """
    Return the last 12 months of precipitation data

    Data in the form:
    [
      {
        "2016-08-23": 0.0
      },
      ...
    ]

    :return: json precipitation data
    """
    last_12_months = session.query(Measurement.date,
                                   Measurement.prcp)\
                        .where(Measurement.date >= ONE_YEAR_PRIOR_DATE)\
                        .order_by(Measurement.date)\
                        .all()
    
    precipitation_dict = [{item.date: item.prcp} for item in last_12_months]
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    stations_dict = {"stations": [value for (value,) in stations]}
    return jsonify(stations_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    most_active_tobs_data = session.query(Measurement.date,
                                          Measurement.tobs)\
                                   .where(Measurement.date >= ONE_YEAR_PRIOR_DATE,
                                          Measurement.station == MOST_ACTIVE_STATION)\
                                   .all()
    most_active_tobs_dict = [{item.date: item.tobs} for item in most_active_tobs_data]
    return jsonify(most_active_tobs_dict)


@app.route("/api/v1.0/<start>")
def start():
    pass


@app.route("/api/v1.0/<start>/<end>")
def start_end_range():
    pass


# Other Functions
def last_date() -> dt.date:
    """Gives the last date of measurements in the database.

    :return: date value
    """
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    return dt.datetime.strptime(most_recent_date, r"%Y-%m-%d").date()


def one_year_prior_date(date_value: dt.date) -> dt.date:
    """Gives a date 1 year before the given date

    :param date_value: date to subtract 1 year from
    :return: 1 year older date
    """
    return date_value - dt.timedelta(days=365)


if __name__ == "__main__":
    app.run(debug=True)
    session.close()
