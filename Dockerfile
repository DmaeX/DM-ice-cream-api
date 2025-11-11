FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install flask --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]