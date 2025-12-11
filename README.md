# Phone-Address Service

Тестовое задание №1 - сервис для хранения связок телефон-адрес на FastAPI и Redis.
<br>
[Тестовое задание №2](https://github.com/malikkhubiev/Test_AVE/blob/main/SecondTask.md)

## Запуск

### С Docker

```bash
docker-compose up --build
```

**Адрес**: http://localhost:8000

### Локально

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Примечание**: Убедитесь, что Redis запущен на `localhost:6379`

## API

**GET** `/phone/{phone}` - получить адрес по телефону

**POST** `/phone` - создать связку
```json
{"phone": "+79001234567", "address": "г. Москва, ул. Ленина, д. 1"}
```

**PUT** `/phone/{phone}` - обновить адрес
```json
{"address": "новый адрес"}
```

**DELETE** `/phone/{phone}` - удалить запись

**GET** `/health` - проверка работы

## Переменные окружения

- `REDIS_HOST` - хост Redis (по умолчанию `localhost`)
- `REDIS_PORT` - порт Redis (по умолчанию `6379`)