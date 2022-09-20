FROM prodgitlab.vodafone.om:5050/shafique.kakati1/test1:latest
MAINTAINER "shafique Kakati" shafiquekakati@gmail.com

RUN pip3 install psycopg2-binary

WORKDIR /app

COPY * /app/

CMD ["python3","/app/multireciever.py"]


