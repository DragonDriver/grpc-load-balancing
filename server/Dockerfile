FROM python:3.6.8-jessie

WORKDIR /server

COPY ./requirements.txt requirements.txt

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY ./*.py ./

# CMD [ "python3", "server.py" ]

CMD [ "tail", "f", "/dev/null" ]

