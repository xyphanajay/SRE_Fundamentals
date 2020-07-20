import random
import redis
import uuid
import time

def main():
    r = redis.Redis(host='localhost', port=9005)
    while True:
        r.zincrby('queue', 1, str(uuid.uuid1()))
        time.sleep(5)

if __name__ == '__main__':
    main()
