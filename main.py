from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FastAPI Starter", version="1.0.0")


class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True


# Simple in-memory storage
items: dict[int, Item] = {}
next_id = 1


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def list_items():
    return [{"id": item_id, **item.model_dump()} for item_id, item in items.items()]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items[item_id].model_dump()}


@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    items[next_id] = item
    result = {"id": next_id, **item.model_dump()}
    next_id += 1
    return result


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return {"id": item_id, **item.model_dump()}


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
