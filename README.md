# Проект Foodgram
**Foodgram** - это сайт, созданный для любителей кулинарии, где пользователи могут делиться своими рецептами, фотографиями блюд и кулинарными идеями. Пользователи могут создавать персональные профили, добавлять в избранное понравившиеся рецепты, подписываться на других авторов, скачивать списки необходимых ингредиентов (список покупок) для приготовления желаемых блюд. Проект помогает научиться готовить интересные блюда, вдохновиться новыми кулинарными идеями и поделиться своими шедеврами с другими любителями еды.

![foodgram](https://github.com/link75/foodgram-project-react/assets/127029704/b286f966-dca4-4569-a762-fb089d5a4d63)

## Технологии, используемые при разработке

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/), [Django REST framework](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.postgresql.org/), [SQLite](https://www.sqlite.org/index.html)
* [React](https://react.dev)
* [Nginx](https://nginx.org/)
* [Docker](https://www.docker.com/)

## Как запустить проект
1. Клонировать репозиторий

```
git clone <адрес_репозитория>
```
```
cd foodgram-project-react
```

2. Создать и активировать виртуальное окружение, обновить (при необходимости) менеджер пакетов pip
```
python -m venv env
source venv/Scripts/activate
python -m pip install --upgrade pip
```
3. Cоздать файл переменных окружения .env по примеру .env.example:
```
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
SECRET_KEY='secret_key'
ALLOWED_HOSTS=localhost,x.x.x.x
DEBUG=False
```
4. Перейти в директорию /backend и установить зависимости из файла requirements.txt
```
cd backend/
pip install -r requirements.txt
```
5. Выполнить миграции
```
python manage.py migrate
```
6. Собрать статические файлы
```
python manage.py collectstatic
```
7. Загрузить начальную базу ингредиентов
```
python manage.py load_ingredients
```
8. Запустить проект:
```
python manage.py runserver
```
На данном этапе вы получите полностью работоспособную часть backend.

Создать суперпользователя
```
python manage.py createsuperuser
```
Панель администратора находится по адресу
```
/admin
```
Сделать тестовые запросы к API

```
/api/ingredients/ - GET-запрос – получение списка всех ингредиентов.
Возможен поиск по частичному вхождению в начале названия ингредиента. Доступно без токена.
```
## Документация к API
```
/api/docs/ - полный список запросов к API
```
## Запуск проекта в Docker контейнерах
1. Установить Docker
```
Параметры запуска описаны в файлах docker-compose.yml и nginx.conf и находятся в директории infra/.
При необходимости отредактируйте файл nginx.conf.
```
2. Собрать контейнеры с помощью Docker Compose
```
docker-compose up -d --build
```
3. Применить миграции
```
docker-compose exec backend python manage.py migrate
```
4. Загрузить ингредиенты
```
docker-compose exec backend python manage.py load_ingredients
```
5. Создать суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```
6. Собрать статические файлы
```
docker-compose exec backend python manage.py collectstatic
```
##



