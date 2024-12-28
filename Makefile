postgres:
	docker run --name postgres_form_builder -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=Debdip123 -e POSTGRES_DB=form_builder -p 5432:5432 -d postgres

createdb:
	docker exec -it postgres_form_builder psql -U admin -d form_builder

dropdb:
	docker exec -it dropdb form_builder

migrateup:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

server:
	python manage.py runserver

.PHONY: postgres createdb dropdb migrateup makemigrations server