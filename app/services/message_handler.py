from sqlalchemy.orm import Session
from app.core.enums import ConversationState
from app.repositories import client_repository as client_repo
from app.services.intent_router import route_intent
from app.services.scheduling_flow import handle_scheduling_step

def process_incoming_message(db: Session, phone_number: str, message: str) -> str:
    """
    Entrypoint principal das regras de negócios.
    Gerencia se o fluxo vai para a maquina de estados ou intent stateless.
    """
    client = client_repo.get_or_create_client(db, phone_number)
    state = ConversationState(client.current_state)
    
    # Se o cliente não estiver em IDLE, ele está no meio de um agendamento.
    # Neste caso, roteamos as mensagens todas para o flow de state-machine.
    if state != ConversationState.IDLE:
        # Permite cancelar o fluxo a qualquer momento
        if message.strip().lower() in ["cancelar", "sair", "parar"]:
            client_repo.update_client_state(db, client, ConversationState.IDLE)
            return "Fluxo de agendamento cancelado. Como posso ajudar agora?"
            
        return handle_scheduling_step(db, client, message)
    
    # Se estiver em IDLE, usa o roteador de intent por palavras-chave
    response = route_intent(message)
    
    if response == "START_SCHEDULING":
        return handle_scheduling_step(db, client, message)
        
    return response

