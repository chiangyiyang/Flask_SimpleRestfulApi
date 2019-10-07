set ip=127.0.0.1
set port=8080
curl -X POST -d "id=a01" -d "lat=23.5" -d "lng=121.5"  http://%IP%:%Port%/devices
curl -X POST -d "id=a02" -d "lat=23.5" -d "lng=121.5"  http://%IP%:%Port%/devices
curl -X POST -d "id=a03" -d "lat=23.5" -d "lng=121.5"  http://%IP%:%Port%/devices

curl -X POST -d "id=a03" -d "t=23.5" -d "h=98.5"  http://%IP%:%Port%/logs
curl -X POST -d "id=a03" -d "t=23.5" -d "h=98.5"  http://%IP%:%Port%/logs

curl http://%IP%:%Port%/devices
curl http://%IP%:%Port%/logs

curl http://%IP%:%Port%/init_db