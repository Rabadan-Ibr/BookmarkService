# BookmarkService
Тестовая работа
#### Инструкция по развертыванию в контейнере.
Скачать репозиторий.\
Выполнить команды из каталога "devops":

Создать образы и развернуть контейнеры.
```commandline
docker compose up -d
```
Выполнить миграции.
```commandline
docker compose exec backend python manage.py migrate
```

Документация: http://127.0.0.1/api/v1/doc/swagger/
