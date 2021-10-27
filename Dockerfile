FROM python:3.8-slim-bullseye

WORKDIR /cmdbot
COPY requirements.txt ./
# RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip3 install -r requirements.txt

COPY . .
COPY .env-prod .env

CMD ["python3", "main.py"]
