from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from contextlib import asynccontextmanager

# --- Models ---

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titel: str
    datum: str

class AppointmentCreate(SQLModel):
    titel: str
    datum: str

class AppointmentRead(SQLModel):
    id: int
    titel: str
    datum: str

class AppointmentUpdate(SQLModel):
    titel: Optional[str] = None
    datum: Optional[str] = None


# --- Database & engine ---

sqlite_url = "sqlite:///afspraken.db"
engine = create_engine(sqlite_url, echo=True)

def get_db():
    with Session(engine) as session:
        yield session

# --- FastAPI + Lifespan (tabellen maken) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


# --- CRUD endpoints ---

@app.post("/appointments/", response_model=AppointmentRead)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@app.get("/appointments/", response_model=List[AppointmentRead])
def read_appointments(db: Session = Depends(get_db)):
    appointments = db.exec(select(Appointment)).all()
    return appointments

@app.get("/appointments/{appointment_id}", response_model=AppointmentRead)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.put("/appointments/{appointment_id}", response_model=AppointmentRead)
def update_appointment(appointment_id: int, payload: AppointmentUpdate, db: Session = Depends(get_db)):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment_data = payload.model_dump(exclude_unset=True)
    for key, value in appointment_data.items():
        setattr(appointment, key, value)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.get(Appointment, appointment_id)
 
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"message": "deleted"}
