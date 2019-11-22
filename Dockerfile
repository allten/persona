FROM python:3.8-alpine

WORKDIR /

EXPOSE 8080

COPY requirements.txt /requirements.txt

RUN apk update
RUN apk add gcc
RUN apk add libc-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY /templates/ /templates/

COPY app.py /app.py

CMD ["python", "app.py"]