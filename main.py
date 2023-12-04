from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Para saber si el RUC existe ir al endpoint /ruc/{ruc}",
            "url": "localhost:8000/ruc/{ruc}"}


@app.get("/ruc/{ruc}")
async def say_hello(ruc: str):
    url = (f"https://srienlinea.sri.gob.ec/sri-catastro-sujeto-servicio-internet/rest/ConsolidadoContribuyente"
           f"/existePorNumeroRuc?numeroRuc={ruc}")
    response = requests.get(url)
    if not response.json():
        return {"ruc": ruc, "existe": False}
    try:
        response.json()['mensaje']
        return {"mensaje": "Posible RUC incorrecto"}
    except TypeError:
        return {"ruc": ruc, "existe": True}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
