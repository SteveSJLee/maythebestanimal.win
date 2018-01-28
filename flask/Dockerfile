FROM python:3.6.4-alpine3.7
MAINTAINER Brett Tegart "bretttegart@gmail.com"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD ./animal_voting /app
WORKDIR /app
CMD ["python", "/usr/local/bin/gunicorn", "--bind=0.0.0.0:8000", "--workers=2", "main:app"]
