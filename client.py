import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

HOSTNAME = 'localhost'
PORT = 1337

ResponseTimes = namedtuple('ResponseTimes', ('short_time', 'long_time'))
Stat = namedtuple('Stat', ('total_time', 'response_times'))


def send_short_request():
    pass


def send_long_request():
    pass


def response_times(nb_requests: int, now=time.time_ns) -> List[ResponseTimes]:
    results = []
    for _ in range(nb_requests):
        start = now()
        send_short_request()
        end_short = now()
        time_short = end_short - start
        send_long_request()
        time_long = now() - end_short
        results.append(ResponseTimes(time_short, time_long))
    return results


def collect_stats(nb_connections: int, nb_requests=10000, now=time.time_ns) -> Stat:
    assert nb_requests % nb_connections == 0
    requests_per_thread = nb_requests//nb_connections
    with ThreadPoolExecutor(max_workers=nb_connections) as executor:
        start = now()
        results = executor.map(response_times, [requests_per_thread for _ in range(nb_connections)])
        total_time = now() - start
    # Flatten the results
    return Stat(total_time, [stats for l in results for stats in l])
