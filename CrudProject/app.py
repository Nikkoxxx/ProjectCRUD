from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hospital Appointment System"}

from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    patient_name: str
    doctor: str
    appointment_datetime: datetime
    reason: str

class Appointment(AppointmentCreate):
    id: int

from typing import List
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

appointments_db = []

@app.post("/appointments/", response_model=Appointment)
def create_appointment(appointment: AppointmentCreate):
    appointment_id = len(appointments_db) + 1
    appointment_model = Appointment(id=appointment_id, **appointment.dict())
    appointments_db.append(appointment_model)
    return appointment_model

@app.get("/appointments/", response_model=List[Appointment])
def get_all_appointments():
    return appointments_db

@app.get("/appointments/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: int):
    appointment = next((a for a in appointments_db if a.id == appointment_id), None)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.put("/appointments/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: int, appointment_update: AppointmentCreate):
    appointment = next((a for a in appointments_db if a.id == appointment_id), None)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.patient_name = appointment_update.patient_name
    appointment.doctor = appointment_update.doctor
    appointment.appointment_datetime = appointment_update.appointment_datetime
    appointment.reason = appointment_update.reason

    return appointment

@app.delete("/appointments/{appointment_id}", response_model=Appointment)
def delete_appointment(appointment_id: int):
    appointment = next((a for a in appointments_db if a.id == appointment_id), None)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointments_db.remove(appointment)
    return appointment

