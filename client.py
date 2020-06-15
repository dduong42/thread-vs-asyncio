import socket
import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

import constants as c

ResponseTimes = namedtuple('ResponseTimes', ('short_time', 'long_time'))
Stat = namedtuple('Stat', ('total_time', 'response_times'))


def send_msg(msg: bytes) -> bool:
    """Send a msg. Returns True on success, False otherwise"""
    sock = socket.create_connection((c.HOSTNAME, c.PORT))
    succeed = True
    try:
        sock.send(msg)
        sock.recv(1)
    except Exception:
        succeed = False
    finally:
        sock.close()
    return True


def response_times(nb_requests: int, now=time.time_ns) -> List[ResponseTimes]:
    results = []
    for _ in range(nb_requests):
        start = now()
        short_succeed = send_msg(c.SHORT)
        end_short = now()
        if short_succeed:
            time_short = end_short - start
        else:
            time_short = None
        long_succeed = send_msg(c.LONG)
        if long_succeed:
            time_long = now() - end_short
        else:
            time_long = None
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
