from pydantic import BaseModel, ConfigDict
from uuid import UUID

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