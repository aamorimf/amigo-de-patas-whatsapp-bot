from sqlalchemy.orm import Session
from app.repositories import client_repository as client_repo
from app.services.state_machine import process_state_machine

def process_incoming_message(db: Session, phone_number: str, message: str) -> str:
    """
    Entrypoint principal das regras de negócios.
    Redireciona todo o tráfego para a rotina da máquina de estados.
    """
    client = client_repo.get_or_create_client(db, phone_number)
    
    return process_state_machine(db, client, message)

