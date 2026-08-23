FROM python:3.11-slim

WORKDIR /app

# Отключаем создание pyc файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Команда по умолчанию (для контейнера bot)
CMD ["python", "bot.py"]
