FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /pizza
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
COPY pizza.py index.py

EXPOSE 5000
CMD [ "python3","-a","flask","run","--host 0.0.0.0"]

