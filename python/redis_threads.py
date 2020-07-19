import argparse
import threading
import redis
import requests
import sys

class CONSTANT():
    url = "http://127.0.0.1:8000"
    local = "localhost"
    queue = "queue"
 

def get_request(data):
	req = requests.get(const.url, data)
	print(" Getting {} .... {} ".format(str(data), str(req)))

def process(redis_obj, const):
    while True:
        try:
            new_data = redis_obj.zrange(const.queue, -1, -1)
            if len(new_data) != 0:
                print(new_data[0])
                redis_obj.zrem(const.queue, new_data[0])
                thread = threading.Thread(target=get_request, args=(new_data[0], const, ))
                thread.start()
        except Exception as ex_err:
            print("-> ERROR: {}".format(ex_err))
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-P', action='store', dest="port", help='Port No., def 6379', default=6379, type=int)

    args = parser.parse_args()
    const = CONSTANT()
    # print(args.port)
    redis_obj =  redis.StrictRedis(host=const.local, args.port)
    process(redis_obj, const)
