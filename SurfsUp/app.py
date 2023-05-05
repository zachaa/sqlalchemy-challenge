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
engine = create_engine("sqlite:///" + str(db_path))
# reflect the database and tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes["measurement"]
Station = Base.classes["station"]

# Create our session (link) from Python to the DB
session = Session(bind=engine)

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
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_prior = dt.datetime.strptime(most_recent_date, r"%Y-%m-%d").date() - dt.timedelta(days=365)
    last_12_months = session.query(Measurement.date,
                                   Measurement.prcp)\
                        .where(Measurement.date >= one_year_prior)\
                        .order_by(Measurement.date)\
                        .all()
    
    precipitation_dict = [{item.date: item.prcp} for item in last_12_months]
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    pass


@app.route("/api/v1.0/tobs")
def tobs():
    pass


@app.route("/api/v1.0/<start>")
def start():
    pass


@app.route("/api/v1.0/<start>/<end>")
def start_end_range():
    pass


if __name__ == "__main__":
    app.run(debug=True)