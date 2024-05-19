# Используем официальный образ Python в качестве базового
FROM python:3.11.4-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /TelegramShop

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения в рабочую директорию
COPY . .

# Определяем команду для запуска вашего приложения
CMD ["python", "bot/main.py"]