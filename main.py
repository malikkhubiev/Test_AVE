from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from redis import Redis
import os
from typing import Dict

app = FastAPI(
    title="Phone-Address Service",
    description="Микросервис для хранения и управления связками телефон-адрес",
    version="1.0.0"
)

# Подключение к Redis
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Возвращает HTML страницу"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/phone/{phone}", status_code=status.HTTP_200_OK)
async def get_address_by_phone(phone: str) -> Dict[str, str]:
    """Получить адрес по телефону"""
    address = redis_client.get(phone)
    
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Телефон {phone} не найден"
        )
    
    return {"phone": phone, "address": address}


@app.post("/phone", status_code=status.HTTP_201_CREATED)
async def create_phone_address(data: Dict[str, str]) -> Dict[str, str]:
    """Создать новую связку телефон-адрес"""
    phone = data.get("phone")
    address = data.get("address")
    
    if not phone or not address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуются поля 'phone' и 'address'"
        )
    
    # Проверяем, существует ли уже такой телефон
    existing_address = redis_client.get(phone)
    
    if existing_address is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Телефон {phone} уже существует"
        )
    
    # Сохраняем новую связку
    redis_client.set(phone, address)
    
    return {"phone": phone, "address": address}


@app.put("/phone/{phone}", status_code=status.HTTP_200_OK)
async def update_phone_address(phone: str, data: Dict[str, str]) -> Dict[str, str]:
    """Обновить адрес по телефону"""
    address = data.get("address")
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется поле 'address'"
        )
    
    # Проверяем, существует ли телефон
    existing_address = redis_client.get(phone)
    
    if existing_address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Телефон {phone} не найден"
        )
    
    # Обновляем адрес
    redis_client.set(phone, address)
    
    return {"phone": phone, "address": address}


@app.delete("/phone/{phone}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_phone_address(phone: str):
    """Удалить запись по телефону"""
    # Проверяем, существует ли телефон
    existing_address = redis_client.get(phone)
    
    if existing_address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Телефон {phone} не найден"
        )
    
    # Удаляем запись
    redis_client.delete(phone)
    
    return None


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Проверка работы сервиса"""
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "redis": "disconnected", "error": str(e)}

