include .env
export $(shell sed 's/=.*//' .env)

postgres:
	docker run --name postgres_form_builder -e POSTGRES_USER=${DB_USER} -e POSTGRES_PASSWORD=${DB_PASSWORD} -e POSTGRES_DB=${DB_NAME} -p ${DB_PORT}:5432 -d postgres

createdb:
	docker exec -it postgres_form_builder createdb -U ${DB_USER} ${DB_NAME}

dropdb:
	docker exec -it postgres_form_builder dropdb -U ${DB_USER} ${DB_NAME}

migrateup:
	cd Backend && python manage.py migrate

makemigrations:
	cd Backend && python manage.py makemigrations

back_server:
	cd Backend && python manage.py runserver

.PHONY: postgres createdb dropdb migrateup makemigrations back_server