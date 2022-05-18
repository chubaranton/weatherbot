FROM ubuntu:latest

COPY . /opt/
WORKDIR /opt/

RUN apt-get update
RUN apt-get install -y\
 python3\
 python3-pip


RUN pip install pyTelegramBotApi
RUN pip install bs4

CMD ["python3", "bot.py"]
