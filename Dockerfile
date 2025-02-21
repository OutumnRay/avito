FROM python:3.13-slim

WORKDIR /backend
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libpq-dev

COPY . .

CMD ["python", "backend/app.py"]
