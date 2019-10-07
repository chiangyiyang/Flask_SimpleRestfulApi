import json
import redis

pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
r = redis.Redis(connection_pool=pool)

locker_key = 'db_locker'
locker_token = 'this is a token'
locker_expire = 3


def lock(key, token, expire):
    return r.set(key, token, nx=True, ex=expire)


def unlock(key, token):
    script = '''
        if redis.call("get",KEYS[1]) == ARGV[1]
        then
            return redis.call("del",KEYS[1])
        else
            return 0
        end    
    '''
    return r.eval(script, 1, key, token)


def save_to_db(**kargs):
    for k, v in kargs.items():
        r.set(k, json.dumps(v))


def load_from_db(*args):
    tmp = ()
    for v in args:
        tmp += (json.loads(r.get(v) or '{}'),)
    return tmp
