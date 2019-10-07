import json
import time
from datetime import datetime

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from db import r, lock, unlock, save_to_db, load_from_db
from db import locker_key, locker_token, locker_expire


app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('lat')
parser.add_argument('lng')
parser.add_argument('t')
parser.add_argument('h')


def abort_if_device_doesnt_exist(device_id):
    if device_id not in Devices:
        abort(404, message="Device {} doesn't exist".format(device_id))


class Device(Resource):
    def get(self, device_id):
        # Testing Cmd: curl http://%IP%:%Port%/devices/a03
        (Devices,) = load_from_db('Devices')
        abort_if_device_doesnt_exist(device_id)
        return Devices[device_id]

    def delete(self, device_id):
        # Testing Cmd: curl -X DELETE http://%IP%:%Port%/devices/a03
        while not lock(locker_key, locker_token, locker_expire):
            pass
        (Devices,) = load_from_db('Devices')
        abort_if_device_doesnt_exist(device_id)
        del Devices[device_id]
        save_to_db(Devices=Devices)
        unlock(locker_key, locker_token)
        return '', 204

    def put(self, device_id):
        # Testing Cmd: curl -X PUT -d "lat=23.0" -d "lng=121.0" http://%IP%:%Port%/devices/a03
        args = parser.parse_args()
        while not lock(locker_key, locker_token, locker_expire):
            pass
        (Devices,) = load_from_db('Devices')
        Devices[device_id] = {'lat': args['lat'], 'lng': args['lng']}
        save_to_db(Devices=Devices)
        unlock(locker_key, locker_token)
        return Devices[device_id], 201

    def patch(self, device_id):
        # Testing Cmd: curl -X PATCH -d "lat=23.5" http://%IP%:%Port%/devices/a03
        while not lock(locker_key, locker_token, locker_expire):
            pass
        (Devices,) = load_from_db('Devices')
        abort_if_device_doesnt_exist(device_id)
        info = Devices[device_id]
        args = parser.parse_args()
        if args['lat'] != None:
            info['lat'] = float(args['lat'])
        if args['lng'] != None:
            info['lng'] = float(args['lng'])

        Devices[device_id] = info
        save_to_db(Devices=Devices)
        unlock(locker_key, locker_token)
        return Devices[device_id], 201


class DeviceList(Resource):
    def get(self):
        # Testing Cmd: curl http://%IP%:%Port%/devices
        (Devices,) = load_from_db('Devices')
        return Devices

    def post(self):
        # Testing Cmd: curl -X POST -d "id=a04" -d "lat=23.5" -d "lng=121.5"  http://%IP%:%Port%/devices
        args = parser.parse_args()
        while not lock(locker_key, locker_token, locker_expire):
            pass
        (Devices,) = load_from_db('Devices')
        if args['id'] in Devices.keys():
            return "ID is duplicated!", 406
        Devices[args['id']] = {'lat': args['lat'], 'lng': args['lng']}
        save_to_db(Devices=Devices)
        unlock(locker_key, locker_token)
        return Devices[args['id']], 201


class LogList(Resource):
    def get(self):
        # Testing Cmd: curl http://%IP%:%Port%/logs
        (Logs,) = load_from_db('Logs')
        return Logs

    def post(self):
        # Testing Cmd: curl -X POST -d "id=a03" -d "t=23.5" -d "h=98.5"  http://%IP%:%Port%/logs
        args = parser.parse_args()
        while not lock(locker_key, locker_token, locker_expire):
            pass
        (Devices, Logs) = load_from_db('Devices', 'Logs')
        if args['id'] not in Devices.keys():
            return "Device %s is not available!" % args['id'], 406
        if args['id'] not in Logs.keys():
            Logs[args['id']] = []
        ts = int(time.time())
        # ts = str(datetime.utcnow())     # datetime.strptime("2019-10-01 14:08:08.774648","%Y-%m-%d %H:%M:%S.%f")
        # if ts in Logs[args['id']].keys():
        #     return "Timestamp is duplicated!", 406
        tmp = Logs[args['id']]
        tmp = tmp[-4:] if len(tmp) >= 4 else tmp
        try:
            tmp = tmp + \
                [{'ts': ts, 't': float(args['t']), 'h': float(args['h'])}, ]
            Logs[args['id']] = tmp
            save_to_db(Logs=Logs)
            unlock(locker_key, locker_token)
            return Logs[args['id']], 201
        except ValueError as err:
            unlock(locker_key, locker_token)
            return {'message': '%r' % err}, 500


class Log(Resource):
    def get(self, device_id):
        # Testing Cmd: curl http://%IP%:%Port%/logs/a03
        (Devices, Logs) = load_from_db('Devices', 'Logs')
        abort_if_device_doesnt_exist(device_id)
        return Logs[device_id]


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<device_id>')
api.add_resource(LogList, '/logs')
api.add_resource(Log, '/logs/<device_id>')


@app.route("/init_db")
def init_db():
    while not lock(locker_key, locker_token, locker_expire):
        pass
    save_to_db(Devices={}, Logs={})
    unlock(locker_key, locker_token)
    return "Database is initialized!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)  # 將IP及Port設定成對外服務
