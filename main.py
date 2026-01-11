from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from decision_engine import can_i_eat

app = FastAPI(
    title="AI Food Decision API",
    description="Explainable food compatibility and recommendation system",
    version="1.0"
)

class User(BaseModel):
    conditions: List[str]
    season: str
    time: str
    digestion: str


class Meal(BaseModel):
    foods: List[str]


class RequestBody(BaseModel):
    user: User
    meal: Meal


@app.post("/can-i-eat")
def analyze_food(data: RequestBody):
    user = data.user.dict()
    meal = data.meal.dict()
    return can_i_eat(user, meal)

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

