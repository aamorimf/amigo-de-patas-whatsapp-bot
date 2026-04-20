from sqlalchemy.orm import Session
from app.models.schema import Appointment
from app.core.enums import AppointmentStatus

def create_draft_appointment(db: Session, client_id: int) -> Appointment:
    # First, cancel any existing drafts for this client
    existing_drafts = db.query(Appointment).filter(
        Appointment.client_id == client_id,
        Appointment.status == AppointmentStatus.DRAFT.value
    ).all()
    for draft in existing_drafts:
        draft.status = AppointmentStatus.CANCELLED.value
    
    appointment = Appointment(client_id=client_id, status=AppointmentStatus.DRAFT.value)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def get_draft_appointment(db: Session, client_id: int) -> Appointment:
    return db.query(Appointment).filter(
        Appointment.client_id == client_id,
        Appointment.status == AppointmentStatus.DRAFT.value
    ).first()

def update_appointment(db: Session, appointment: Appointment):
    db.commit()
    db.refresh(appointment)
