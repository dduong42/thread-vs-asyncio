import os.path
import signal
import subprocess
from contextlib import contextmanager


@contextmanager
def service(latency: int):
    # latency is in ms
    path = os.path.abspath('service.py')
    with subprocess.Popen([path, str(latency)], stdout=subprocess.PIPE) as proc:
        yield
        proc.send_signal(signal.SIGTERM)


@contextmanager
def async_server(latency: int):
    with service(latency):
        # latency is in ms
        path = os.path.abspath('async_server.py')
        with subprocess.Popen([path], stdout=subprocess.PIPE) as proc:
            yield
            proc.send_signal(signal.SIGTERM)


if __name__ == '__main__':
    with async_server(10000):
        input()
