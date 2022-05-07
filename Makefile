install:
	poetry install
lint:
	poetry run flake8
test:
	poetry run python3 manage.py test
sort:
	poetry run isort .
start:
	poetry run python3 manage.py runserver
shell:
	poetry run python3 manage.py shell
make_migrations:
	poetry run python3 manage.py makemigrations
migrate:
	poetry run python3 manage.py migrate
export_req:
	poetry export -f requirements.txt --output requirements.txt
flush_db:
	poetry run python3 manage.py flush 