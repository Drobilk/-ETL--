from flask import Flask, request, jsonify
import psycopg2
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# настройка логирования
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# загрузка переменных окружения из файла .env
load_dotenv()

# параметры подключения к базе данных из переменных окружения
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# создание курсора для выполнения запросов
conn = psycopg2.connect(
    dbname=db_params['dbname'],
    user=db_params['user'],
    password=db_params['password'],
    host=db_params['host'],
    port=5432
)
cur = conn.cursor()

# REST API метод для поиска по индексу
@app.route('/search')
def search():
    app.logger.info('search request received')
    # получение параметров запроса из URL
    city_from = request.args.get('city_from')
    city_to = request.args.get('city_to')
    # выполнение запроса в базу данных
    cur.execute("""
        SELECT *
        FROM flights_tickets_passengers_mv
        WHERE from_city = %s AND to_city = %s
    """, (city_from, city_to))
    # получение результатов запроса
    results = cur.fetchall()
    # формирование и отправка ответа
    return jsonify(results)

# запуск приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
