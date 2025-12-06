from fastapi import FastAPI
from pydantic import BaseModel

class Afspraak(BaseModel):
    titel:str
    datum:str

app = FastAPI()
data=[
        {"titel":"dokter",
         "jaar":"2000",
         "maand":"july",
         "dag":"8"},
        {"titel":"school",
         "jaar":"2000",
         "maand":"july",
         "dag":"8"},
        {"titel":"werk",
         "jaar":"2000",
         "maand":"july",
         "dag":"8"}
     ]


@app.get("/")
async def root():
    return data
@app.post("/")
async def create_item(afspraak:Afspraak):
    data.append(afspraak)
    return afspraak