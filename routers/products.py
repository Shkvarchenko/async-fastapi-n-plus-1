from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID

from database import get_db
from models import Product, Review, User
from schemas import CreateItem, UpdateItem, ItemSchema
from dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/items", response_model=list[ItemSchema])
async def get_all_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()


@router.post("/items", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: CreateItem, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_item = Product(
        name=payload.name,
        price=payload.price,
        stock=payload.stock
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@router.patch("/items/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: UUID, 
    payload: UpdateItem, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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


@router.put("/items/{item_id}", response_model=ItemSchema)
async def put_item(
    item_id: UUID, 
    payload: CreateItem, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = await db.get(Product, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="item_not_found")
        
    product.name = payload.name
    product.price = payload.price
    product.stock = payload.stock
    
    await db.commit()
    await db.refresh(product)
    return product


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = await db.get(Product, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="item_not_found")
    
    await db.delete(product)
    await db.commit()
    return None


# ==========================================
# N+1 Query Demonstration (Демонстрация)
# ==========================================

@router.get("/bad")
async def get_products_bad(db: AsyncSession = Depends(get_db)):
    """BAD PRACTICE: Triggers the N+1 query problem."""
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


@router.get("/good")
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