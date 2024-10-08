FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]