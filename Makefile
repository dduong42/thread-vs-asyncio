.POSIX:
db.sqlite3: createdb.sql
	sqlite3 db.sqlite3 < createdb.sql

isort:
	isort *.py

mypy:
	mypy *.py

qa: isort mypy

clean:
	rm -f db.sqlite3
