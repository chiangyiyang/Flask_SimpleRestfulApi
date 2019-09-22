from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Devices(Resource):
    def get(self):
        # 回傳3組測試資料
        return [                    
            {'id':'aa01', 'lat':23.51, 'lng':121.31},
            {'id':'aa02', 'lat':23.52, 'lng':121.32},
            {'id':'aa03', 'lat':23.53, 'lng':121.33}]

api.add_resource(Devices, '/devices')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)  # 將IP及Port設定成對外服務