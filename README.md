Для запуска необходимо создать файл .env в папке проекта и задать следующие переменные:

Данные для доступа к БД:

- DB_NAME=
- DB_USERNAME=
- DB_PASSWORD=

Заполнение данными из db.json:

- python manage.py loaddata db.json 

Ссылки для проверки:
- /courses
- /payment/?ordering=date
- /payment/?course=3
- /payment/?lesson=3

