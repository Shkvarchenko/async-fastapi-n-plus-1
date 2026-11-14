from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
# ИМПОРТИРУЕМ РОУТЕР
from routers import products

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting server. Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("Shutting down server...")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"]
)

# ПОДКЛЮЧАЕМ РОУТЕР ТОВАРОВ
app.include_router(products.router)