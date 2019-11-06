FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /

COPY Requirements.txt /Requirements.txt

# RUN apk add --update python py-pip python-dev
# RUN apk add make automake gcc g++ subversion python3-dev
# RUN apk --no-cache add ca-certificates

# RUN pip3 install --upgrade pip
# RUN pip3 install docker --user
# RUN pip3 install predix==0.0.8 --user


RUN apk update
RUN apk add gcc
RUN apk add libc-dev

RUN pip install --upgrade pip
RUN pip install -r Requirements.txt

COPY index.html /templates/index.html

COPY app.py /app.py

CMD ["python", "app.py"]
