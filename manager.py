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
