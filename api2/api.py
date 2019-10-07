import time
from datetime import datetime

from flask_restful import Resource, Api, reqparse, abort
from sqlalchemy import exc

from .main import app
from . import models

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('latitude')
parser.add_argument('longitude')
parser.add_argument('temperature')
parser.add_argument('humidity')
parser.add_argument('device_id')


def abort_if_device_doesnt_exist(device_id):
    models.Device.query.filter_by(
        id=device_id).first_or_404(description="Device %s doesn't exist" % device_id)


class Device(Resource):
    def get(self, device_id):
        # Testing Cmd: curl http://%IP%:%Port%/devices/1
        abort_if_device_doesnt_exist(device_id)
        return models.Device.query.filter_by(id=device_id).first().json()

    def delete(self, device_id):
        # Testing Cmd: curl -X DELETE http://%IP%:%Port%/devices/1
        query = models.Device.query.filter_by(id=device_id)
        model = query.first_or_404(
            description="Device %s doesn't exist" % device_id)
        models.db.session.delete(model)
        models.db.session.commit()
        return {'message': 'Done'}, 200

    def put(self, device_id):
        # Testing Cmd: curl -X PUT -d "name=a001" -d "latitude=23.0" -d "longitude=121.0" http://%IP%:%Port%/devices/1
        args = parser.parse_args()
        model = models.Device.query.filter_by(id=device_id).first()
        if model is None:
            model = models.Device(name=args['name'],
                                  longitude=args['longitude'],
                                  latitude=args['latitude'])
        else:
            model.name = args['name'] or model.name
            model.longitude = args['longitude'] or model.longitude
            model.latitude = args['latitude'] or model.latitude
        models.db.session.add(model)
        try:
            models.db.session.commit()
            return model.json(), 201
        except exc.IntegrityError as e:
            return {"message": "ERROR: The name:%r is duplicated!" % args['name']}, 500

    def patch(self, device_id):
        # Testing Cmd: curl -X PATCH -d "name=a001" http://%IP%:%Port%/devices/1
        args = parser.parse_args()
        model = models.Device.query.filter_by(id=device_id).first_or_404(
            description="Device %s doesn't exist" % device_id)
        model.name = args['name'] or model.name
        model.longitude = args['longitude'] or model.longitude
        model.latitude = args['latitude'] or model.latitude
        models.db.session.add(model)
        try:
            models.db.session.commit()
            return model.json(), 201
        except exc.IntegrityError as e:
            return {"message": "ERROR: The name:%r is duplicated!" % args['name']}, 500
        except exc.StatementError as e:
            return {"message": e._message()}, 500


class DeviceList(Resource):
    def get(self):
        # Testing Cmd: curl http://%IP%:%Port%/devices
        return [d.json() for d in models.Device.query.all()]

    def post(self):
        # Testing Cmd: curl -X POST -d "name=a04" -d "latitude=23.5" -d "longitude=121.5"  http://%IP%:%Port%/devices
        args = parser.parse_args()
        model = models.Device(
            name=args['name'], longitude=args['longitude'], latitude=args['latitude'])
        models.db.session.add(model)
        try:
            models.db.session.commit()
            return model.json(), 201
        except exc.IntegrityError as e:
            return {"message": "ERROR: The name:%r is duplicated!" % args['name']}, 500


class LogList(Resource):
    def get(self):
        # Testing Cmd: curl http://%IP%:%Port%/logs
        return [d.json() for d in models.DhtLog.query.all()]

    def post(self):
        # Testing Cmd: curl -X POST -d "device_id=1" -d "temperature=23.5" -d "humidity=98.5"  http://%IP%:%Port%/logs
        args = parser.parse_args()
        abort_if_device_doesnt_exist(args['device_id'])
        model = models.DhtLog(
            timestamp=datetime.utcnow(),
            temperature=args['temperature'],
            humidity=args['humidity'],
            device_id=args['device_id'])
        models.db.session.add(model)
        try:
            models.db.session.commit()
            return model.json(), 201
        except exc.StatementError as e:
            return {"message": e._message()}, 500


class Log(Resource):
    def get(self, device_id):
        # Testing Cmd: curl http://%IP%:%Port%/devices/1
        abort_if_device_doesnt_exist(device_id)
        return [d.json() for d in models.DhtLog.query.filter_by(device_id=device_id).all()]


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<device_id>')
api.add_resource(LogList, '/logs')
api.add_resource(Log, '/logs/<device_id>')
