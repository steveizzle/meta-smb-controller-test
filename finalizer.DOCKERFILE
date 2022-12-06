FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir kubernetes

COPY ./finalize.py ./finalize.py

EXPOSE 8080

CMD [ "python", "./finalize.py" ]