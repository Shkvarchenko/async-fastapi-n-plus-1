Простой REST API для управления инвентарем предметов.
Сделан на fastAPI+Pydantic.

## Стек
- python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- UUID

## Функционал
- GET /items - получить все предметы
- GET /items/{id} - получить предмет по ID (c обработкой 404)
- POST /items - добавить новый предмет (генерируется UUID, "is_rare" опционально)
- PATCH /items/{id} - частично обновить предмет (только переданные поля)
- DELETE /items/{id} - удалить предмет (статус 204)

## 🏁 Инструкция по локальному запуску

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com
   cd fastapi-items-inventory
   ```

2. **Установите все зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Запустите сервер uvicorn:**
   ```bash
   uvicorn code34:app --reload
   ```

4. **Откройте интерактивную документацию:**
   Перейдите в браузере по адресу  http://127.0.0