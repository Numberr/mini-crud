Простое CRUD для управления пользователями на FastAPI с использованием PostgreSQL

Функционал:
- Создание пользователя
- Получение пользователя по ID
- Обновление данных пользователя
- Удаление пользователя
- Валидация возраста

Использованы технологии:
- FastAPI
- PostgreSQL
- psycopg2
- Pydantic
- Uvicorn

Запуск локально:
1. Установка зависимостей
  pip install -r requirements.txt
  
2. Настройка переменных окружения
  Создайте файл .env на основе .env.example

3. Создайте базу данных
  CREATE SCHEMA lesson_1;
  CREATE TABLE lesson_1.users (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      lastname TEXT NOT NULL,
      password TEXT NOT NULL,
      birthday TIMESTAMP NOT NULL
  );

4. Запуск приложения
   python main.py

После запуска API будет доступен по адресу: http://127.0.0.1:8000/docs
