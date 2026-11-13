# 🇬🇧 Async FastAPI Backend with N+1 Demonstration / 🇷🇺 Асинхронный бэкенд на FastAPI

A robust, fully asynchronous REST API built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL**. 

This project demonstrates modern backend development best practices, including asynchronous database sessions, Docker containerization with health checks, and a practical comparison of the **N+1 query problem** versus the optimal eager loading approach (`selectinload`).

Надежный, полностью асинхронный REST API, построенный с использованием **FastAPI**, **SQLAlchemy 2.0** и **PostgreSQL**.

Этот проект демонстрирует лучшие практики современной бэкенд-разработки: асинхронные сессии баз данных, контейнеризацию через Docker с проверкой здоровья (healthcheck), а также наглядное сравнение **проблемы N+1** с оптимальным подходом жадной загрузки (`selectinload`).

## 🛠 Tech Stack / Стек технологий

*   **Framework:** FastAPI
*   **Database:** PostgreSQL 15
*   **ORM:** SQLAlchemy 2.0 (Async)
*   **Containerization:** Docker & Docker Compose
*   **Validation:** Pydantic v2
*   **Driver:** asyncpg

## ✨ Key Features / Ключевые особенности

*   **100% Asynchronous:** Uses `AsyncSession` and `async/await` for non-blocking I/O operations.
*   **Dockerized Environment:** Includes a `docker-compose.yml` with a PostgreSQL `healthcheck` to ensure the web app starts only when the database is fully ready.
*   **N+1 Problem Solution:** Includes specific endpoints (`/products_bad` vs `/products_good`) to demonstrate how to optimize database queries using `selectinload`.
*   **UUIDs as Primary Keys:** Uses UUIDv4 for product IDs to improve scalability and security.
*   **Clean Architecture:** Separated database configuration, models, and routes.

*   **100% Асинхронность:** Используются `AsyncSession` и `async/await` для неблокирующих операций ввода-вывода.
*   **Docker-окружение:** В `docker-compose.yml` настроен `healthcheck` для PostgreSQL, чтобы веб-приложение запускалось только после полной готовности базы данных.
*   **Решение проблемы N+1:** В проекте есть специальные эндпоинты (`/products_bad` и `/products_good`), которые демонстрируют, как оптимизировать запросы к базе данных с помощью `selectinload`.
*   **UUID в качестве первичных ключей:** Для ID товаров используются UUIDv4 для улучшения масштабируемости и безопасности.
*   **Чистая архитектура:** Конфигурация БД, модели и роуты разделены по файлам.

## 🚀 How to Run / Как запустить локально

### Prerequisites / Требования
*   Docker and Docker Compose installed.

### Installation / Установка

1. Clone the repository / Клонируйте репозиторий:
   `git clone https://github.com/Shkvarchenko/YOUR_REPO_NAME.git`
   `cd YOUR_REPO_NAME`

2. Set up environment variables / Настройте переменные окружения:
   `cp .env.example .env`

3. Start the containers / Запустите контейнеры:
   `docker compose up -d --build`

4. Access the API / Доступ к API:
   The interactive Swagger UI will be available at / Интерактивная документация Swagger доступна по адресу:
   👉 http://localhost:8000/docs

### Optional: Seed Test Data / Заполнение базы тестовыми данными

To populate the database with products and reviews for testing the N+1 endpoints, run the seed script **inside the web container**:
Чтобы наполнить базу товарами и отзывами для тестирования эндпоинтов N+1, запустите скрипт **внутри контейнера**:

`docker exec -it fastapi-app python seed.py`

## 📡 API Endpoints / Эндпоинты API

### Products CRUD / CRUD для товаров
*   `GET /items` — Get a list of all products / Получить список всех товаров.
*   `POST /items` — Create a new product / Создать новый товар.
*   `PATCH /items/{item_id}` — Partially update a product / Частично обновить товар.
*   `PUT /items/{item_id}` — Fully replace a product / Полностью заменить товар.
*   `DELETE /items/{item_id}` — Delete a product / Удалить товар.

### N+1 Query Demonstration / Демонстрация проблемы N+1
*   `GET /products_bad` — Fetches data using the **inefficient way** (1 query + N queries). Check logs using `docker logs fastapi-app`.
*   `GET /products_good` — Fetches data using `selectinload`, resulting in exactly **2 queries** total.

*   `GET /products_bad` — Получает данные **неэффективным способом** (1 запрос + N запросов). Посмотрите логи командой `docker logs fastapi-app`.
*   `GET /products_good` — Получает данные с помощью `selectinload`, что дает ровно **2 запроса** в базу.

## 📁 Project Structure / Структура проекта

*   `database.py` — Async engine, session, settings, and Base / Асинхронный движок, сессии и Base.
*   `main.py` — FastAPI app, models, schemas, and routes / Приложение, модели, схемы и роуты.
*   `seed.py` — Script to populate the database / Скрипт заполнения базы.
*   `docker-compose.yml` — Docker services with healthcheck / Docker-сервисы с проверкой.
*   `Dockerfile` — Web app container instructions / Инструкции для контейнера.
*   `.env.example` — Environment variables template / Шаблон переменных окружения.
