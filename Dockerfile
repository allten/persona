FROM python:3.8-alpine

WORKDIR /chat

COPY Requirements.txt /chat/Requirements.txt

COPY index.html /chat/templates/index.html

COPY app.py /chat/app.py

RUN apk add build-base libffi-dev

RUN pip install -r Requirements.txt


CMD ["python", "app.py"]
