import socket
import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from typing import List

import constants as c

ResponseTimes = namedtuple(
    'ResponseTimes',
    ('start_time', 'end_short_time', 'end_time', 'short_succeeded', 'long_succeeded')
)
Stats = namedtuple(
    'Stats',
    ('start_time', 'end_time', 'response_times')
)


def send_msg(msg: bytes) -> bool:
    """Send a msg. Returns True on success, False otherwise"""
    succeed = True
    try:
        # 1 second timeout
        sock = socket.create_connection((c.HOSTNAME, c.PORT), timeout=1)
    except Exception:
        return False
    try:
        sock.send(msg)
        sock.recv(1)
    except Exception:
        succeed = False
    finally:
        sock.close()
    return succeed


def response_times(nb_requests: int, now=time.time_ns) -> List[ResponseTimes]:
    results = []
    for _ in range(nb_requests):
        start = now()
        short_succeeded = send_msg(c.SHORT)
        end_short = now()
        long_succeeded = send_msg(c.LONG)
        end = now()
        results.append(ResponseTimes(start, end_short, end, short_succeeded, long_succeeded))
    return results


def collect_stats(nb_connections: int, nb_requests=9000, now=time.time_ns) -> Stats:
    requests_per_thread = nb_requests//nb_connections
    inputs = [requests_per_thread for _ in range(nb_connections)]
    inputs[-1] += nb_requests % nb_connections
    assert sum(inputs) == nb_requests
    start = now()
    with ThreadPoolExecutor(max_workers=nb_connections) as executor:
        results = executor.map(response_times, inputs)
    end = now()
    return Stats(start, end, results)
