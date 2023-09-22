# from src import status_db, store_info_db
from src import db

class Timezones(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer)
    timezone_str = db.Column(db.Text)

class Store_status(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer)
    status = db.Column(db.Text)
    timestamp_utc = db.Column(db.Text)

class Store_hours(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer)
    day = db.Column(db.Integer)
    start_time_local = db.Column(db.Text)
    end_time_local = db.Column(db.Text)