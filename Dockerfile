FROM python:3.10-slim

COPY Requirements.txt .

RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

EXPOSE 5500

CMD gunicorn --workers=2 --bind 0.0.0.0:5500 'application:app'