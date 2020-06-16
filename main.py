#!/usr/bin/env python3

import sqlite3
import time

from client import collect_stats
from manager import async_server

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

for latency in range(100, 1100, 100):
    for nb_connections in range(10, 110, 10):
        print('latency: {}, nb_connections: {}'.format(latency, nb_connections))
        with async_server(latency):
            # Wait for the servers to be ready
            time.sleep(0.5)
            stats = collect_stats(nb_connections)
        cursor.execute(
            '''INSERT INTO stats (latency, nb_connections, start_time, end_time)
               VALUES (?, ?, ?, ?)''',
            (latency, nb_connections, stats.start_time, stats.end_time)
        )
        stat_id = cursor.lastrowid
        for thread_id, response_times in enumerate(stats.response_times):
            for rt in response_times:
                cursor.execute(
                    '''INSERT INTO stats_results (stat_id, thread_id, start_time, end_short_time, end_time, short_succeeded, long_succeeded)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (stat_id, thread_id, rt.start_time, rt.end_short_time, rt.end_time, rt.short_succeeded, rt.long_succeeded)
                )
        conn.commit()
