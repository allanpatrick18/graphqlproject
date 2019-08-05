FROM python:3.6.5

MAINTAINER ALLAN

# copy source code from app folder to docker image
RUN mkdir -p /opt/backend/app
COPY . /opt/backend/app

# define workdir
WORKDIR /opt/backend/app

# Print python output to docker logs
ENV PYTHONUNBUFFERED 1

# Environment variables
ENV DJANGO_SETTINGS_MODULE backend_test.settings
ENV PORT 8080


# install requirements
RUN pip install -Ur requirements.txt

RUN useradd -c 'app user' -m -s /bin/bash app
RUN chown -R app.app /opt/backend/app
RUN mkdir /var/www
RUN chown -R app.app /var/www
USER app

EXPOSE  8080

CMD ["/bin/bash", "-c", "python manage.py runserver 0.0.0.0:8080"]
