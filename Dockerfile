FROM python:3.8.0-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /app .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:api", "--reload"]

