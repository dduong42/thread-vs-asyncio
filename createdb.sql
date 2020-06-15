CREATE TABLE IF NOT EXISTS stats (
	latency INTEGER NOT NULL,
	nb_connections INTEGER NOT NULL,
	nb_threads INTEGER NOT NULL,
	total_time INTEGER NOT NULL,
	PRIMARY KEY (latency, nb_connections, nb_threads)
);
CREATE TABLE IF NOT EXISTS stat_results (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	latency INTEGER NOT NULL,
	nb_connections INTEGER NOT NULL,
	nb_threads INTEGER NOT NULL,
	short_time INTEGER,
	long_time INTEGER,
	FOREIGN KEY (latency, nb_connections, nb_threads) REFERENCES stats(latency, nb_connections, nb_threads)
);
