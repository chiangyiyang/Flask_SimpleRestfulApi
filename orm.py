
import os

from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)
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
        return '<Device %r (%r, %r)>' % (self.name, self.longitude, self.latitude)


class DhtLog(db.Model):
    __tablename__ = 'dht_logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))

    def __repr__(self):
        return '<DhtLog %r %r %r>' % (self.timestamp, self.temperature, self.humidity)
    


if __name__ == '__main__':
    manager.run()