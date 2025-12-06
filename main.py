from fastapi import FastAPI
from pydantic import BaseModel, AfterValidator
from typing import Optional, Annotated
import sqlite3

conn=sqlite3.connect("afspraken.db")
conn.row_factory = sqlite3.Row   
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS afspraken (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titel TEXT NOT NULL,
    datum TEXT NOT NULL
)
""")
conn.commit()
def lang_genoeg(titel:str):
    assert len(titel)>3 , "titel te kort"
    return titel
Titel=Annotated[str,AfterValidator(lang_genoeg)]
class Afspraak(BaseModel):
    id:Optional[int]=None
    titel:Titel
    datum:str

app = FastAPI()


@app.get("/")
async def root():
    afspraken=cursor.execute("select * from afspraken").fetchall()
    return [dict(row) for row in afspraken]
@app.post("/")
async def create_item(afspraak:Afspraak):
    cursor.execute("insert into afspraken(titel,datum) values (?,?)",[afspraak.titel,afspraak.datum])
    conn.commit()
    return afspraak
@app.delete("/")
async def delete_item(id_item:int):
    cursor.execute("DELETE FROM afspraken WHERE id = ?", (id_item,))
    conn.commit()
    return "verwijdert"