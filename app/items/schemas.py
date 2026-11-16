from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["Laptop"])
    price: float = Field(gt=0, examples=[999.99])
    in_stock: bool = True


class ItemCreate(ItemBase):
    """Body for POST /items. Clients don't send an id."""


class ItemUpdate(ItemBase):
    """Body for PUT /items/{id}. Replaces the whole item."""


class ItemRead(ItemBase):
    """What the API returns. Includes the server-assigned id."""

    id: int
