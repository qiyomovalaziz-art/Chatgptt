# Python 3.11 ishlatamiz
FROM python:3.11-slim

WORKDIR /app

# Dependencies o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App fayllarini nusxalash
COPY . .

# Botni ishga tushiramiz
CMD ["python", "main.py"]
