from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
class Afspraak(BaseModel):
    id:Optional[int]=None
    titel:str
    datum:str

app = FastAPI()
data=[]
id=1

@app.get("/")
async def root():
    return data
@app.post("/")
async def create_item(afspraak:Afspraak):
    global id
    afspraak.id=id
    id+=1
    data.append(afspraak)
    return afspraak
@app.delete("/")
async def delete_item(id_item:int):
    for index, item in enumerate(data):
        if item.id == id_item:
            data.pop(index)
    return "verwijdert"