Some docker configure file, Dockerfile, stored in this repository.

Reference: 
- <https://github.com/huchenw/django-docker>


# django-docker
A complete example for deploying Django project with Nginx and MariaDB on Docker, see [django-py35](https://github.com/OnlyBelter/docker-repo/tree/master/django-py35) & running R package through `rpy2` package in Python environment, see [rpy2-docker](https://github.com/OnlyBelter/docker-repo/tree/master/rpy2-docker).

## QuickStart
Install Docker Engine from the tutorial <https://docs.docker.com/engine/installation/>.</br>
Install Docker Compose from the tutorial <https://docs.docker.com/compose/install/>.</br>
Get the latest project clone to your computer:
```bash
$ git clone git@github.com:OnlyBelter/docker-repo.git
```
Build image:
```
cd django-py35
docker build -t onlybelter/django_py35 .
```
Run docker-compose commands to start containers:
```bash
$ docker-compose up -d
```

## Django Admin
If you want to access django admin site, please apply the django default migrations to database:
```bash
$ docker-compose exec web bash
$ python manage.py migrate
```
Then you need to create a superuser account:
```bash
$ python manage.py createsuperuser
```

## Docker Images Reference

| Name   | Image                              |
| ------ | ---------------------------------- |
| nginx:1.12.2-alpine  | <https://hub.docker.com/_/nginx/>  |
| mariadb:5.5  | <https://hub.docker.com/_/mariadb/>  |
| rpy2/rpy2:2.9.x  | <https://hub.docker.com/r/rpy2/rpy2/>  |
| python:3.5-alpine | <https://hub.docker.com/_/python/> |

