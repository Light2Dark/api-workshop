from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from enum import Enum
from ai import predict_coin_neural_net
import requests

templates = Jinja2Templates(directory="templates")

class Coin(str, Enum):
    dogecoin = "dogecoin-Elon"
    bitcoin = "bitcoin-2"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/coins")
async def get_coins_from_coingecko():
    response = requests.get("https://api.coingecko.com/api/v3/coins/list?include_platform=false")
    return response.json()

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("main.html", {"request": request, "id": id})

@app.get("/coins/{coin_id}")
async def get_coin(coin_id: str):
    return {
        "coin": {
            "id": coin_id,
            "name": "Dogecoin"
        }
    }
    
@app.get("/get_enum_coins/{enum_coin}")
async def get_enum_coin(enum_coin: Coin):
    return {
        "coin": {
            "id": enum_coin,
            "name": enum_coin.bitcoin
        }
    }
    
@app.get("/coin_price/{coin_id}")
async def get_coin_price_range(coin_id: str, start_date: str, end_date: str):
    return {
        "coin": {
            "id": coin_id,
            "name": "Dogecoin",
            "price": 0.123
        }
    }
    
@app.get("/predict_price/{coin_id}")
async def predict_coin_price(coin_id: str):    
    response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=myr&from=1679809739&to=1680414539")
    prices = response.json().get('prices', [])
    price_list = [price[1] for price in prices]
    
    next_price = predict_coin_neural_net(price_list)
    return {
        "coin": coin_id,
        "next_price": str(next_price)
    }