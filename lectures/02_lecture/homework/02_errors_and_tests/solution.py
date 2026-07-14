"""
02_errors_and_tests — чиним и тестируем 🛠️

В app.py лежит сломанное FastAPI-приложение. Найдите и исправьте ВСЕ проблемы.

Задача А: Исправить приложение (task.py)
    Скопируйте app.py сюда и исправьте все ошибки.
    Внимание: tests будут проверять ВАШУ реализацию, не оригинальный app.py.

    Чего ждут тесты:
        ✓ POST /items → 201 Created
        ✓ GET  /items/{id} → 200 или 404
        ✓ PUT  /items/{id} → 200 или 404
        ✓ DELETE /items/{id} → 204 или 404
        ✓ GET  /divide?a=10&b=0 → 400 (не 500!)
        ✓ GET  /items/{id}/counter → race condition отсутствует
        ✓ GET  /slow-sync → async def + await asyncio.sleep
        ✓ DELETE возвращает правильный статус (204)

Задача Б: Написать тесты в test_errors.py
    Покрыть все эндпоинты.
"""

import asyncio
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel

app = FastAPI()

ITEMS: dict[int, dict] = {}
NEXT_ID = 1
COUNTER = 0


class ItemCreate(BaseModel):
    name: str


class ItemUpdate(BaseModel):
    name: str = ""


# ═══════════════════════════════════════════════════════════
# ИСПРАВЛЯЙТЕ НИЖЕ
# ═══════════════════════════════════════════════════════════


@app.get("/items")
def list_items():
    return {"items": list(ITEMS.values())}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    # TODO:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    return ITEMS[item_id]


@app.post("/items", status_code=201)
def create_item(item: ItemCreate):
    # TODO:
    global NEXT_ID
    new_item = {"id": NEXT_ID, "name": item.name}
    ITEMS[NEXT_ID] = new_item
    NEXT_ID += 1
    return new_item


@app.get("/items/{item_id}/counter")
def get_counter(item_id: int):
    # TODO:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    global COUNTER
    COUNTER += 1
    return {"counter": COUNTER}


@app.put("/items/{item_id}")
def update_item(item_id: int, update: ItemUpdate):
    # TODO:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    
    ITEMS[item_id]["name"] = update.name
    return ITEMS[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # TODO:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del ITEMS[item_id]
    return Response(status_code=204)


@app.get("/divide")
def divide(a: int, b: int):
    # TODO:
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": a / b}


@app.get("/slow-sync")
async def slow_sync():
    # TODO:
    await asyncio.sleep(0.5)
    return {"status": "done"}