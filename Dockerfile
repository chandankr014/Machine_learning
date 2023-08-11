FROM python:3.10-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8855

CMD gunicorn --workers=2 --bind 0.0.0.0:8855 'app:app'