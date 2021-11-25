FROM python:3.8-slim-bullseye

WORKDIR /cmdbot
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
COPY .env-prod .env

ENV PORT=3000

EXPOSE 3000

CMD ["python3", "main.py", "&", "python3", "api.py"]
