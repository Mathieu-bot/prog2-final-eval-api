from typing import List
from fastapi import FastAPI, HTTPException
from starlette.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI(title="STD24192", version="1.0.0")

@app.get("/health")
def get_health():
    return PlainTextResponse(content="Ok")

class Characteristic(BaseModel):
    ram_memory: int
    rom_memory: int

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

phones: List[Phone] = []

@app.post("/phones", status_code=201)
def post_phones(phone: Phone):
    phones.append(phone)
    return phone

@app.get("/phones")
def get_phones():
    return phones

@app.get("/phones/{id}")
def get_phone(id: str):
    for phone in phones:
        if phone.identifier == id:
            return phone
    raise HTTPException(status_code=404, detail=f"The phone with id {id} was not found")

@app.put("/phones/{id}/characteristics")
def put_phone_characteristics(id: str, characteristics: Characteristic):
    for i, phone in enumerate(phones):
        if phone.identifier == id:
            phone.characteristics = characteristics
            phones[i] = phone
            return phone
    raise HTTPException(status_code=404, detail=f"The phone with id {id} was not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)