from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, select, create_engine
from typing import Optional
from contextlib import asynccontextmanager

# -----------------------------------
# SQLModel ORM klasse
# -----------------------------------
class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titel: str
    datum: str


# -----------------------------------
# Database Engine + sessie-provider
# -----------------------------------
engine = create_engine("sqlite:///afspraken.db", echo=True)

def get_db():
    with Session(engine) as session:
        yield session


# -----------------------------------
# Lifespan: tabellen aanmaken
# -----------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
# -----------------------------------
# GET: alle afspraken
# -----------------------------------
@app.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    result = db.exec(select(Appointment)).all()
    return result


# -----------------------------------
# GET: één afspraak op ID
# -----------------------------------
@app.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Afspraak niet gevonden")
    return appointment


# -----------------------------------
# POST: afspraak toevoegen
# -----------------------------------
@app.post("/appointments")
def create_appointment(afspraak: Appointment, db: Session = Depends(get_db)):
    db.add(afspraak)
    db.commit()
    db.refresh(afspraak)
    return afspraak


# -----------------------------------
# DELETE: afspraak verwijderen
# -----------------------------------
@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Afspraak niet gevonden")

    db.delete(appointment)
    db.commit()
    return {"message": "verwijderd"}
