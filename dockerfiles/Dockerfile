#syntax=docker/dockerfile:1.2
FROM python:3.8-slim-buster
WORKDIR /Users/sophiasangervasi/Documents/dockerfiles
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3","-u","Wallie.py"]
