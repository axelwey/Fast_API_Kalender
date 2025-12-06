from fastapi import FastAPI
from sqlmodel import SQLModel, Field, Session, select, create_engine
from typing import Optional

# ------------------------------------
# SQLModel ORM Klasse
# ------------------------------------
class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titel: str
    datum: str

# ------------------------------------
# Database
# ------------------------------------
engine = create_engine("sqlite:///afspraken.db", echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ------------------------------------
# FastAPI
# ------------------------------------
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/appointments")
def get_appointments():
    with Session(engine) as session:
        statement = select(Appointment)
        results = session.exec(statement).all()
        return results

@app.post("/appointments")
def create_appointment(afspraak: Appointment):
    with Session(engine) as session:
        session.add(afspraak)
        session.commit()
        session.refresh(afspraak)
        return afspraak

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    with Session(engine) as session:
        appointment = session.get(Appointment, appointment_id)
        if not appointment:
            return {"error": "Appointment not found"}

        session.delete(appointment)
        session.commit()
        return {"message": "deleted"}
