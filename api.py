from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import time

app = Flask(__name__)
api = Api(app)

Devices = {'a01': {'lat': 23.51, 'lng': 121.31},
           'a02': {'lat': 23.52, 'lng': 121.32},
           'a03': {'lat': 23.53, 'lng': 121.33}}

Logs = {
    'a01': {
        '001': {'t': 24, 'h': 91},
        '002': {'t': 25, 'h': 92},
        '003': {'t': 26, 'h': 93},
        '004': {'t': 27, 'h': 94},
        '005': {'t': 28, 'h': 95}},
    'a02': {
        '001': {'t': 24, 'h': 91},
        '002': {'t': 25, 'h': 92},
        '003': {'t': 26, 'h': 93},
        '004': {'t': 27, 'h': 94},
        '005': {'t': 28, 'h': 95}},
    'a03': {
        '001': {'t': 24, 'h': 91},
        '002': {'t': 25, 'h': 92},
        '003': {'t': 26, 'h': 93},
        '004': {'t': 27, 'h': 94},
        '005': {'t': 28, 'h': 95}}
}

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('lat')
parser.add_argument('lng')
parser.add_argument('t')
parser.add_argument('h')


def abort_if_device_doesnt_exist(device_id):
    if device_id not in Devices:
        abort(404, message="Device {} doesn't exist".format(device_id))

# Device
# shows a single Device item and lets you delete a Device item


class Device(Resource):
    def get(self, device_id):
        # Testing Cmd: curl http://%IP%:%Port%/devices/a03
        abort_if_device_doesnt_exist(device_id)
        return Devices[device_id]

    def delete(self, device_id):
        # Testing Cmd: curl -X DELETE http://%IP%:%Port%/devices/a03
        abort_if_device_doesnt_exist(device_id)
        del Devices[device_id]
        return '', 204

    def put(self, device_id):
        # Testing Cmd: curl -X PUT -d "lat=23.0" -d "lng=121.0" http://%IP%:%Port%/devices/a03
        args = parser.parse_args()
        Devices[device_id] = {'lat': args['lat'], 'lng': args['lng']}
        return Devices[device_id], 201

    def patch(self, device_id):
        # Testing Cmd: curl -X PATCH -d "lat=23.0" http://%IP%:%Port%/devices/a03
        abort_if_device_doesnt_exist(device_id)
        info = Devices[device_id]
        args = parser.parse_args()
        if args['lat'] != None:
            info['lat'] = float(args['lat'])
        if args['lng'] != None:
            info['lng'] = float(args['lng'])

        Devices[device_id] = info
        return Devices[device_id], 201


class DeviceList(Resource):
    def get(self):
        # Testing Cmd: curl http://%IP%:%Port%/devices
        return Devices

    def post(self):
        # Testing Cmd: curl -X POST -d "id=a04" -d "lat=23.5" -d "lng=121.5"  http://%IP%:%Port%/devices
        args = parser.parse_args()
        if args['id'] in Devices.keys():
            return "ID is duplicated!", 406
        Devices[args['id']] = {'lat': args['lat'], 'lng': args['lng']}
        return Devices[args['id']], 201


class LogList(Resource):
    def get(self):
        # Testing Cmd: curl http://%IP%:%Port%/logs
        return Logs

    def post(self):
        # Testing Cmd: curl -X POST -d "id=a04" -d "t=23.5" -d "h=98.5"  http://%IP%:%Port%/logs
        args = parser.parse_args()
        if args['id'] not in Devices.keys():
            return "Device %s is not available!" % args['id'], 406
        if args['id'] not in Logs.keys():
            Logs[args['id']] = {}
        ts = int(time.time())
        if ts in Logs[args['id']].keys():
            return "Timestamp is duplicated!", 406
        tmp = Logs[args['id']]
        tmp[ts] = {'t': args['t'], 'h': args['h']}
        Logs[args['id']] = tmp
        return Logs[args['id']], 201


class Log(Resource):
    def get(self, device_id):
        # Testing Cmd: curl http://%IP%:%Port%/devices/a03
        abort_if_device_doesnt_exist(device_id)
        return Logs[device_id]


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<device_id>')
api.add_resource(LogList, '/logs')
api.add_resource(Log, '/logs/<device_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)  # 將IP及Port設定成對外服務
