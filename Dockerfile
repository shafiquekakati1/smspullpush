FROM prodgitlab.vodafone.om:5050/shafique.kakati1/test1:latest
MAINTAINER "shafique Kakati" shafiquekakati@gmail.com


WORKDIR /app

COPY *.py /app

CMD ["python3","/app/multireciever.py"]


