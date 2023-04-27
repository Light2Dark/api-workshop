from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pandas as pd
import json
from sklearn.linear_model import LinearRegression
from fastapi.templating import Jinja2Templates
from utils import get_state_symbol

templates = Jinja2Templates(directory="templates")

df_deforestation = pd.read_csv("amazon_rainforest/def_area_2004_2019.csv")
df_deforestation.rename(columns={"Ano/Estados": "Year"}, inplace=True)
df_deforestation.index = df_deforestation["Year"]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/deforestation")
async def get_deforestation(year: int = 2019):
    row = df_deforestation.loc[df_deforestation["Year"] == year]
    row = row.to_json(orient="records")

    response = json.loads(row)[0]
    return response


@app.get("/deforestation/{state}")
async def get_deforestation_state(state: str):
    """
    States available: Acre, Amazonas, Amapa, Para, Maranhao, Rondonia, Roraima, Tocantins, Mato Grosso
    """
    state_symbol = get_state_symbol(state)
    if state_symbol is None:
        return {"message": "State not found"}
    
    return df_deforestation[state_symbol].to_dict()


@app.get("/predict_deforestation")
async def predict_deforestation(state: str = None):
    """
    By default, provides overall deforestation for next year. If state is provided, provides prediction for that state.
    """
    state_symbol = get_state_symbol(state)
    df = df_deforestation[state_symbol] if state else df_deforestation["AMZ LEGAL"]
    
    x, y = df.index, df.values
    model = LinearRegression()
    model.fit(x.values.reshape(-1, 1), y)

    predictions = {}
    for year in range(2020, 2025):
        predictions[year] = model.predict([[year]])[0]
    
    return predictions


@app.get("/visualize", response_class=HTMLResponse)
async def read_item(request: Request, state: str):
    predictions = get_predictions(state)
    return templates.TemplateResponse("amazon.html", {"request": request, "state": state, "predictions": predictions})


def get_predictions(state: str) -> list:
    state_symbol = get_state_symbol(state)
    df = df_deforestation[state_symbol] if state else df_deforestation["AMZ LEGAL"]
    
    x, y = df.index, df.values
    model = LinearRegression()
    model.fit(x.values.reshape(-1, 1), y)

    predictions = {}
    for year in range(2020, 2025):
        predictions[year] = model.predict([[year]])[0]
    
    return predictions