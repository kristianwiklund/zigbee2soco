FROM ubuntu:20.04
RUN apt-get update && apt-get -y install --no-install-recommends python3 python3-pip
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install paho-mqtt
RUN pip3 install soco
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 
COPY zigbee2soco.py /
ENTRYPOINT ["/zigbee2soco.py"]
