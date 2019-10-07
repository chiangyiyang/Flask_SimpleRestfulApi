import time
import random
import redis

pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
r = redis.Redis(connection_pool=pool)

# lock_token = random.randint(1,100000)
# lock_key = "my:lock"
# lock_expire = 3


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


def do_jobs():
    key = 'lock_something'
    token = 1234
    expire = 4
    if lock(key, token, expire):
        print('Locked')
        import time
        time.sleep(3)
        print('Job is Done!!')
        if unlock(key, token):
            print('Unlocked')
        return True
    return False

while not do_jobs():
    time.sleep(1)
    print('Try again...')
