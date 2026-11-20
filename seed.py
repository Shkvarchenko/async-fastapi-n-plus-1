import asyncio
from database import async_session, engine, Base
from models import Product, Review

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        p1 = Product(name="Laptop", price=1000)
        p2 = Product(name="Smartphone", price=500)
        p3 = Product(name="Headphones", price=100)
        session.add_all([p1, p2, p3])
        await session.commit()

        r1 = Review(text="Great laptop, very fast!", product_id=p1.id)
        r2 = Review(text="Gets a bit hot...", product_id=p1.id)
        r3 = Review(text="Good screen quality", product_id=p2.id)
        r4 = Review(text="Battery drains fast", product_id=p2.id)
        r5 = Review(text="Loud and clear sound", product_id=p3.id)
        
        session.add_all([r1, r2, r3, r4, r5])
        await session.commit()
        print("✅ Database seeded successfully with test data!")

if __name__ == "__main__":
    asyncio.run(seed_data())