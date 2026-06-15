from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Lab API", version="1.0.0")


class Item(BaseModel):
    id: int
    name: str
    price: float


# In-memory "database" just for this lab
items_db: dict[int, Item] = {}


@app.get("/")
def root():
    return {"message": "Hello from FastAPI on Amazon Linux! Updated Version 3"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/items", status_code=201)
def create_item(item: Item):
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.id] = item
    return item


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.get("/items")
def list_items():
    return list(items_db.values())