import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

HOSTNAME = 'localhost'
PORT = 1337


def send_short_request():
    pass


def send_long_request():
    pass


def response_times(nb_requests: int, now=time.time_ns) -> List[Tuple[int, int]]:
    results = []
    for _ in range(nb_requests):
        start = now()
        send_short_request()
        end_short = now()
        time_short = end_short - start
        send_long_request()
        time_long = now() - end_short
        results.append((time_short, time_long))
    return results


def collect_stats(nb_connections: int, nb_requests=10000) -> List[Tuple[int, int]]:
    assert nb_requests % nb_connections == 0
    requests_per_thread = nb_requests//nb_connections
    with ThreadPoolExecutor(max_workers=nb_connections) as executor:
        results = executor.map(response_times, [requests_per_thread for _ in range(nb_connections)])
    # Flatten the results
    return [stats for l in results for stats in l]
