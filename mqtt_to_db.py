import json
import time
import paho.mqtt.client as mqtt
from db import r, lock, unlock, save_to_db, load_from_db
from db import locker_key, locker_token, locker_expire


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("yiyang/logs/#")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = msg.payload.decode('utf-8')
    args = json.loads(data)
    while not lock(locker_key, locker_token, locker_expire):
        pass
    (Devices, Logs) = load_from_db('Devices', 'Logs')
    if args['id'] not in Devices.keys():
        print("Device %s is not available!" % args['id'])
        return
    if args['id'] not in Logs.keys():
        Logs[args['id']] = []
    ts = int(time.time())
    tmp = Logs[args['id']]
    tmp = tmp[-4:] if len(tmp) >= 4 else tmp
    try:
        tmp = tmp+[{'ts': ts, 't': float(args['t']), 'h': float(args['h'])}, ]
        Logs[args['id']] = tmp
        save_to_db(Logs=Logs)
        unlock(locker_key, locker_token)
        print('Device %s added a log.' % args['id'])
    except ValueError as err:
        unlock(locker_key, locker_token)
        print('Error: %r \n when device %s adding a log.' % (err, args['id']))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)
client.loop_forever()
