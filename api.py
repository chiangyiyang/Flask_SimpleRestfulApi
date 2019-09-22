from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

Devices = {'a01':{'lat': 23.51, 'lng': 121.31},
           'a02':{'lat': 23.52, 'lng': 121.32},
           'a03':{'lat': 23.53, 'lng': 121.33}}

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('lat')
parser.add_argument('lng')

class DeviceList(Resource):
    def get(self):      
        #Testing Cmd: curl http://IP:Port/devices 
        return Devices    

    def post(self):     
        #Testing Cmd: curl -X POST -d "id=a04" -d "lat=23.5" -d "lng=121.5"  http://IP:Port/devices  
        args = parser.parse_args()
        if  args['id'] in Devices.keys():
            return "ID id duplicated!", 406
        Devices[args['id']] = {'lat': args['lat'], 'lng': args['lng']}
        return Devices[args['id']], 201

api.add_resource(DeviceList, '/devices')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)  # 將IP及Port設定成對外服務
