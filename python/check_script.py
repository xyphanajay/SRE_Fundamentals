import argparse
import requests
import sys

class CONSTANT():
    url = "https://play.grafana.org/api/datasources/proxy/1/render?target=aliasByNode(movingAverage(scaleToSeconds(apps.fakesite.*.counters.requests.count,%201),%202),%202)&format=json&from=-5min"
    critical = "Critical"
    warn = "Warning"
    target = "target"
    datapoints = "datapoints"


def api_call(url):
    '''
    makes api call to url
    :url:
    '''
    print("-> Making api request . . .")
    try:
        data = requests.get(url).json()
    except ConnectionError as conn_err:
        print("~> ERROR: Connection error. {}".format(conn_err))
        data = []
    return data


def check_status(data_set, critical, warning, const):
    ret_code = 0
    # print(data_set)
    for data in data_set:
        target = data[const.target]
        for val in data[const.datapoints]:
            if float(val[0]) >= warning:
                ret_code = 1
                print("$ Val: {}".format(float(val[0])))
                if float(val[0]) >= critical:
                    ret_code = 2
    return ret_code

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--critical', '-C', action='store', dest='crit', help='Critical memory threshold value, eg. 90', default=90, type=int)
    parser.add_argument('--warn', '-W', action='store', dest='warn', help='Warning memory threshold value, eg. 80', default=80, type=int)

    args = parser.parse_args()
    exit_code = 0
    const = CONSTANT()
    result = api_call(const.url)
    if result == []:
        print("-> Unable to fetch dta")
        exit_code = 1
    else:
        exit_code = check_status(result, args.crit, args.warn, const)
    print("-> Status code: {}".format(exit_code))
    sys.exit(exit_code)
