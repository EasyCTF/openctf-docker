FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y install python python-pip libjpeg-dev python-dev libmysqlclient-dev memcached tmux python-nose

RUN mkdir /openctf
COPY . /openctf/
WORKDIR /openctf

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "4", "app:app"]
EXPOSE 8000