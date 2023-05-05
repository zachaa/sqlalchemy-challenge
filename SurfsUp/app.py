from flask import Flask, jsonify
from sqlalchemy import create_engine, desc, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
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


if __name__ == "__main__":
    app.run(debug=True)