from fastapi import HTTPException, status, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from uuid import UUID
import uuid
from pydantic import BaseModel, ConfigDict
from database import engine, get_db, Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]
    stock: Mapped[int] = mapped_column(default=0)
    
    reviews: Mapped[list["Review"]] = relationship(back_populates="product")

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255))
    
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="reviews")

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

class CreateItem(BaseModel):
    name: str
    price: int
    stock: int = 0
    
class UpdateItem(BaseModel):
    name: str | None = None
    price: int | None = None
    stock: int | None = None

class ItemSchema(CreateItem):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

@app.get("/items", response_model=list[ItemSchema])
async def get_all_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()

@app.post("/items", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(payload: CreateItem, db: AsyncSession = Depends(get_db)):
    new_item = Product(
        name=payload.name,
        price=payload.price,
        stock=payload.stock
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@app.patch("/items/{item_id}", response_model=ItemSchema)
async def update_item(item_id: UUID, payload: UpdateItem, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="item_not_found")
        
    if payload.name is not None:
        product.name = payload.name
    if payload.price is not None:
        product.price = payload.price
    if payload.stock is not None:
        product.stock = payload.stock
        
    await db.commit()
    await db.refresh(product)
    return product

@app.put("/items/{item_id}", response_model=ItemSchema)
async def put_item(item_id: UUID, payload: CreateItem, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="item_not_found")
        
    product.name = payload.name
    product.price = payload.price
    product.stock = payload.stock
    
    await db.commit()
    await db.refresh(product)
    return product

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="item_not_found")
    
    await db.delete(product)
    await db.commit()
    return None

@app.get("/products_bad")
async def get_products_bad(db: AsyncSession = Depends(get_db)):
    """BAD PRACTICE: Triggers the N+1 query problem (many redundant queries)."""
    result = await db.execute(select(Product))
    products = result.scalars().all()
    
    response = []
    for p in products:
        stmt = select(Review).where(Review.product_id == p.id)
        reviews_result = await db.execute(stmt)
        reviews = reviews_result.scalars().all()
        
        response.append({
            "name": p.name,
            "reviews": [r.text for r in reviews]
        })
    return response

@app.get("/products_good")
async def get_products_good(db: AsyncSession = Depends(get_db)):
    """GOOD PRACTICE: Solves the N+1 problem using selectinload (only 2 queries)."""
    stmt = select(Product).options(selectinload(Product.reviews))
    result = await db.execute(stmt)
    products = result.scalars().all()
    
    response = []
    for p in products:
        response.append({
            "name": p.name,
            "reviews": [r.text for r in p.reviews]
        })
    return response