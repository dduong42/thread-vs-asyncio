CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	latency INTEGER NOT NULL,
	nb_connections INTEGER NOT NULL,
	nb_threads INTEGER,
	start_time INTEGER NOT NULL,
	end_time INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS stats_results (
    stat_id INTEGER NOT NULL REFERENCES stats(id),
	thread_id INTEGER NOT NULL,
	start_time INTEGER NOT NULL,
	end_short_time INTEGER NOT NULL,
	end_time INTEGER NOT NULL,
	short_succeeded BOOLEAN NOT NULL,
	long_succeeded BOOLEAN NOT NULL,
	PRIMARY KEY (stat_id, thread_id, start_time)
);
