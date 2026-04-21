from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from app.core.enums import ConversationState

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    current_state = Column(
        String,
        nullable=False,
        default=ConversationState.INICIO.value
    )

class Quote(Base):
    __tablename__ = 'quotes'
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    setor = Column(String, nullable=True)
    produto = Column(String, nullable=True)
    tamanho = Column(String, nullable=True)
    quantidade = Column(String, nullable=True)
    status = Column(String, nullable=False, default="DRAFT")