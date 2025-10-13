FROM python:3.12-slim

WORKDIR /app

COPY data/data.csv data/data.csv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY gppd_assisstant .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]