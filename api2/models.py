
import os
import json

from flask_sqlalchemy import SQLAlchemy

from .main import app

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] =\
    "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLAlCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    dht_logs = db.relationship('DhtLog', backref='device')

    def __repr__(self):
        return '<Device id:%r name:%r (%r, %r)>' % (self.id, self.name, self.longitude, self.latitude)

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'longitude': self.longitude,
                'latitude': self.latitude}


class DhtLog(db.Model):
    __tablename__ = 'dht_logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))

    def __repr__(self):
        return '<DhtLog id:%r timestamp:%s temperature:%r humidity:%r>' % (
            self.id, self.timestamp, self.temperature, self.humidity)

    def json(self):
        return {'id': self.id,
                'timestamp': str(self.timestamp),
                'temperature': self.temperature,
                'humidity': self.humidity,
                'device_id': self.device_id}


models = {'Device': Device, 'DhtLog': DhtLog}
