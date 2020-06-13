import socket
import time
import constants as c
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

ResponseTimes = namedtuple('ResponseTimes', ('short_time', 'long_time', 'short_succeed', 'long_succeed'))
Stat = namedtuple('Stat', ('total_time', 'response_times'))


def send_msg(msg: bytes) -> bool:
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


def send_short_request() -> bool:
    """Send a short request. Returns True on success, False otherwise"""
    return send_msg(c.SHORT)


def send_long_request() -> bool:
    """Send a long request. Returns True on success, False otherwise"""
    return send_msg(c.LONG)


def response_times(nb_requests: int, now=time.time_ns) -> List[ResponseTimes]:
    results = []
    for _ in range(nb_requests):
        start = now()
        short_succeed = send_short_request()
        end_short = now()
        time_short = end_short - start
        long_succeed = send_long_request()
        time_long = now() - end_short
        results.append(ResponseTimes(time_short, time_long, short_succeed, long_succeed))
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
