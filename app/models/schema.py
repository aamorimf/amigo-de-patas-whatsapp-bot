from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    current_state = Column(String, nullable=False, default="IDLE")

class IncomingMessage(BaseModel):
    phone: str
    text: str

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    tutor_name = Column(String, nullable=True)
    pet_name = Column(String, nullable=True)
    service_type = Column(String, nullable=True)
    preferred_date = Column(String, nullable=True)
    preferred_time = Column(String, nullable=True)
    status = Column(String, nullable=False, default="DRAFT")
