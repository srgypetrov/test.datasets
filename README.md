Склонировать проект:

```
git clone srgypetrov@bitbucket.org:srgypetrov/alytics.git
```

Запуск django:

```
python manage.py runserver
```

Запуск celery:

```
celery worker -A core -n worker1 -Q first,second,third,celery
```

Запуск flower:

```
flower -A core
```
