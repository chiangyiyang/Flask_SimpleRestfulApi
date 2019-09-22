from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

Devices = {'a01':{'lat': 23.51, 'lng': 121.31},
           'a02':{'lat': 23.52, 'lng': 121.32},
           'a03':{'lat': 23.53, 'lng': 121.33}}

class DeviceList(Resource):
    def get(self):      
        #Testing Cmd: curl http://IP:Port/devices 
        return Devices    

api.add_resource(DeviceList, '/devices')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)  # 將IP及Port設定成對外服務
