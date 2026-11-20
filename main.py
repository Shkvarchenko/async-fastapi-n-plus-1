from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
from routers import products, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting server...")
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
app.include_router(products.router)
app.include_router(auth.router)