# Import necessary libraries

from sqlalchemy import create_engine
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import inspect

from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import (
    Flask,
    render_template,
    jsonify,
    redirect)

import pandas as pd
import numpy as np
import os

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# #################################################
# # flask setup
# #################################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"


# #################################################
# # database setup
# #################################################
#db = SQLAlchemy(app)

#engine = create_engine(os.environ.get('DATABASE_URL', '') or "sqlite:///db/belly_button_biodiversity.sqlite")
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")

conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#samples = Base.classes.samples

Sample = Base.classes.samples
Metadata = Base.classes.samples_metadata
Otu = Base.classes.otu

# Create our session (link) from Python to the DB
session = Session(engine)


# #################################################
# # tables setup
# #################################################
#class Otu(db.Model):
# class Otu(Base):
#     """docstring for Otu"""
#     __tablename__ = "otu"
#     # otu_id = db.Column(db.Integer, primary_key=True)
#     # lowest_taxonomic_unit_found = db.Column(db.String)
#     otu_id = Column(Integer, primary_key=True)
#     lowest_taxonomic_unit_found = Column(String)


# class Metadata(db.Model):
# #class Metadata(Base):
#     __tablename__ = "samples_metadata"
#     sampleid = db.Column(db.Integer, primary_key=True)
#     event = db.Column(db.String)
#     ethnicity = db.Column(db.String)
#     gender = db.Column(db.String)
#     age = db.Column(db.Integer)
#     wfreq = db.Column(db.Float)
#     bbtype = db.Column(db.String)
#     location = db.Column(db.String)
#     country012 = db.Column(db.String)
#     zip012 = db.Column(db.Integer)
#     country1319 = db.Column(db.String)
#     zip1319 = db.Column(db.Integer)
#     dog = db.Column(db.String)
#     cat = db.Column(db.String)
#     impsurface013 = db.Column(db.Integer)
#     npp013 = db.Column(db.Float)
#     mmaxtemp013 = db.Column(db.Float)
#     pfc013 = db.Column(db.Float)
#     impsurface1319 = db.Column(db.Integer)
#     npp1319 = db.Column(db.Float)
#     mmaxtemp1319 = db.Column(db.Float)
#     pfc1319 = db.Column(db.Float)

    # sampleid = Column(Integer, primary_key=True)
    # event = Column(String)
    # ethnicity = Column(String)
    # gender = Column(String)
    # age = Column(Integer)
    # wfreq = Column(Float)
    # bbtype = Column(String)
    # location = Column(String)
    # country012 = Column(String)
    # zip012 = Column(Integer)
    # country1319 = Column(String)
    # zip1319 = Column(Integer)
    # dog = Column(String)
    # cat = Column(String)
    # impsurface013 = Column(Integer)
    # npp013 = Column(Float)
    # mmaxtemp013 = Column(Float)
    # pfc013 = Column(Float)
    # impsurface1319 = Column(Integer)
    # npp1319 = Column(Float)
    # mmaxtemp1319 = Column(Float)
    # pfc1319 = Column(Float)
# #################################################
# # routes configurations
# #################################################
@app.route("/")
def home():
    """Return the dashboard homepage."""
    return render_template("index.html")

# """List of sample names.
    # Returns a list of sample names in the format
    # [
    #     "BB_940",
    #     "BB_941",
    #     "BB_943",
    #     "BB_944",
    #     "BB_945",
    #     "BB_946",
    #     "BB_947",
    #     ...
    # ]
   
@app.route('/names')
def names():
   
    sample_names = []
    inspector = inspect(engine)
    columns = iter(inspector.get_columns('samples'))
    next(columns)

    for column in columns:
        sample_names.append(column['name'])

    return jsonify(sample_names)

# Returns a list of OTU descriptions in the following format
#     [
#         "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
#         "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
#         "Bacteria",
#         "Bacteria",
#         "Bacteria",
#         ...
#     ]
    
@app.route('/otu')
def otu():
   
    #low_units_list = db.session.query(Otu.lowest_taxonomic_unit_found).all()
    low_units_list = session.query(Otu.lowest_taxonomic_unit_found).all()
    low_units = [l[0] for l in low_units_list]
    return jsonify(low_units)


#    MetaData for a given sample.
#     Args: Sample in the format: `BB_940`
#     Returns a json dictionary of sample metadata in the format
#     {
#         AGE: 24,
#         BBTYPE: "I",
#         ETHNICITY: "Caucasian",
#         GENDER: "F",
#         LOCATION: "Beaufort/NC",
#         SAMPLEID: 940
#     }
#     
@app.route('/metadata/<sample>')
@app.route('/metadata')
def metadata(sample="None"):
 
    metadata = []


    for i in session.query(Metadata.AGE, Metadata.BBTYPE, Metadata.ETHNICITY, Metadata.GENDER, Metadata.LOCATION, Metadata.SAMPLEID).all():
        sample_item = {}

        sample_item['SAMPLEID'] = i[5]
        sample_item['AGE'] = i[0]
        sample_item['BBTYPE'] = i[1]
        sample_item['ETHNICITY'] = i[2]
        sample_item['GENDER'] = i[3]
        sample_item['LOCATION'] = i[4]
        

        metadata.append(sample_item)

    for selection in metadata:
        if sample[3:] == str(selection['SAMPLEID']):
            return jsonify(selection)

    return jsonify(metadata)


#   Weekly Washing Frequency as a number.
#     Args: Sample in the format: `BB_940`
#     Returns an integer value for the weekly washing frequency `WFREQ`

@app.route("/wfreq/<sample>")
def wfrequency(sample):
    sample_name = sample.replace("BB_", "")
    sample_conv = int(sample_name)
    result = session.query(Metadata.WFREQ).filter_by(SAMPLEID = sample_conv).all()
    wash_freq = result[0][0]
    return jsonify(wash_freq)


# OTU IDs and Sample Values for a given sample.
#     Sort your Pandas DataFrame (OTU ID and Sample Value)
#     in Descending Order by Sample Value
#     Return a list of dictionaries containing sorted lists  for `otu_ids`
#     and `sample_values`

@app.route('/samples/<sample>')
# @app.route('/samples')
#def samples(sample="None"):
def samples(sample):   
    
    sample_query = sample
    result = session.query(Sample.otu_id, sample_query).order_by(desc(sample_query)).all()
    otu_ids = [result[x][0] for x in range(len(result))]
    sample_values = [result[x][1] for x in range(len(result))]
    dict_list = [{"otu_ids": otu_ids}, {"sample_values": sample_values}]
    return jsonify(dict_list)    

if __name__ == "__main__":
    app.run()
