FROM python:3.9
LABEL maintainer="Dylan Turnbull <dylanturnb@gmail.com>"

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./src /repolytics

CMD [ "python", "repolytics/app.py" ]