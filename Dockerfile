#FROM python:3.9-slim-buster
#FROM ubuntu:18.04
FROM python:3.10-slim


RUN apt-get update -y
RUN apt-get install zip -y
RUN apt-get install wget -y
#RUN apt-get install llvm-7 -y
#RUN apt-get -y install llvm-11*

RUN mkdir /app
RUN mkdir /app/flaskapp
COPY flaskapp /app/flaskapp

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install --upgrade wheel setuptools

COPY requirements.txt /app
COPY run.py /app
COPY gunicorn.sh /app
COPY init.sql /app
COPY *.zip /app
COPY *.sav /app


#RUN apt-get install -y libmariadb-dev
#RUN apt-get install -y gcc

WORKDIR /app
RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1fVjqg2tgdvB0LNHmIdpkHoQidq9sZ1oP' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1fVjqg2tgdvB0LNHmIdpkHoQidq9sZ1oP" -O outlier_model.sav && rm -rf /tmp/cookies.txt

RUN pip install -r requirements.txt
#RUN unzip model.zip 

EXPOSE 5005
#CMD python run.py
RUN ["chmod", "+x", "./gunicorn.sh"]

ENTRYPOINT ["./gunicorn.sh"]
