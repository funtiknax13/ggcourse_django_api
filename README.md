Для запуска необходимо создать файл .env в папке проекта и задать следующие переменные:

```
Ключ STRIPE

- STRIPE_KEY
```
Заполнение данными из db.json:
```
- python manage.py loaddata db.json 
```

Ссылки для проверки:
```
- /courses
- /payment/?ordering=date
- /payment/?course=3
- /payment/?lesson=3
- /course/2/pay/ (Оплата через stripe)
```
_Для создания образа из Dockerfile и запуска контейнера:_
```
docker compose build
docker compose up
```
_Для применения миграций в контейнере:_
```
docker compose exec app python manage.py migrate
```
