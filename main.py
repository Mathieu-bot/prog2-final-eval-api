from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import PlainTextResponse

app = FastAPI(title="STD24192", version="1.0.0")

@app.get("/health")
def get_health():
    return PlainTextResponse(content="Ok")

phones = {}

@app.post("/phones", status_code=201)
def post_phones(phone: dict):
    identifier = phone.get("identifier")
    if not identifier:
        return JSONResponse(content={"error": "identifier is required"}, status_code=400)
    phones[identifier] = phone
    return phone

@app.get("/phones")
def get_phones():
    return list(phones.values())

@app.get("/phones/{id}")
def get_phone(id: str):
    phone = phones.get(id)
    if phone is None:
        return JSONResponse(content={"error": f"The phone with id {id} was not found"}, status_code=404)
    return phone

@app.put("/phones/{id}/characteristics")
def put_phone_characteristics(id: str, characteristics: dict):
    phone = phones.get(id)
    if phone is None:
        return JSONResponse(content={"error": f"The phone with id {id} was not found"}, status_code=404)

    characteristics = characteristics.get("characteristics", {})
    phone["characteristics"] = {
        "ram_memory": characteristics.get("ram_memory"),
        "rom_memory": characteristics.get("rom_memory"),
    }
    phones[id] = phone
    return phone


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)