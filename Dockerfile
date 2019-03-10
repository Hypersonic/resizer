FROM debian:stretch

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

WORKDIR /opt/resize
COPY ./templates/* ./templates/
COPY ./requirements.txt ./
COPY ./server.py ./

RUN pip3 install -r requirements.txt

CMD ["python3", "server.py"]
