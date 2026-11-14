from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
import uuid
from database import Base

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