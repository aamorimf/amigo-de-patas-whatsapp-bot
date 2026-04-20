from sqlalchemy.orm import Session
from app.models.schema import Client
from app.core.enums import ConversationState, AppointmentStatus
from app.repositories import client_repository as client_repo
from app.repositories import appointment_repository as appt_repo
from app.utils.text_parser import is_valid_service_type, is_valid_date, is_valid_time

def handle_scheduling_step(db: Session, client: Client, message: str) -> str:
    state = ConversationState(client.current_state)
    
    # Se estivesse em IDLE, quem chamou isso cometeu erro, mas por precaução:
    if state == ConversationState.IDLE:
        appt_repo.create_draft_appointment(db, client.id)
        client_repo.update_client_state(db, client, ConversationState.WAITING_TUTOR_NAME)
        return "Ótimo! Para começarmos o agendamento, qual é o seu nome?"
        
    draft = appt_repo.get_draft_appointment(db, client.id)
    if not draft:
        # Se por algum motivo estourou, reseta.
        client_repo.update_client_state(db, client, ConversationState.IDLE)
        return "Tivemos um problema com seu agendamento, vamos começar de novo. Digite 'agendar'."

    if state == ConversationState.WAITING_TUTOR_NAME:
        draft.tutor_name = message.strip()
        appt_repo.update_appointment(db, draft)
        client_repo.update_client_state(db, client, ConversationState.WAITING_PET_NAME)
        return f"Prazer, {draft.tutor_name}! Qual é o nome do seu pet?"
        
    elif state == ConversationState.WAITING_PET_NAME:
        draft.pet_name = message.strip()
        appt_repo.update_appointment(db, draft)
        client_repo.update_client_state(db, client, ConversationState.WAITING_SERVICE_TYPE)
        return f"Entendido. O que o(a) {draft.pet_name} precisa hoje? (Consulta, Vacina ou Exames)"
        
    elif state == ConversationState.WAITING_SERVICE_TYPE:
        if not is_valid_service_type(message):
            return "Por favor, seja um pouco mais específico. Ele precisa de uma 'Consulta', 'Vacina' ou 'Exame'?"
        draft.service_type = message.strip()
        appt_repo.update_appointment(db, draft)
        client_repo.update_client_state(db, client, ConversationState.WAITING_DATE)
        return "Perfeito! Para qual data? (ex: hoje, amanha, quarta, 15/04)"
        
    elif state == ConversationState.WAITING_DATE:
        if not is_valid_date(message):
            return "Data inválida ou muito vaga. Por favor digite algo como: 'hoje', 'amanha', 'quinta' ou '15/04'."
        draft.preferred_date = message.strip()
        appt_repo.update_appointment(db, draft)
        client_repo.update_client_state(db, client, ConversationState.WAITING_TIME)
        return "E qual período ou horário de preferência? (ex: manha, tarde, 15h, 10:30)"
        
    elif state == ConversationState.WAITING_TIME:
        if not is_valid_time(message):
            return "Horário inválido ou vago. Por favor responda com algo mais exato: 'manha', 'tarde', '14h', '10:30'."
        draft.preferred_time = message.strip()
        draft.status = AppointmentStatus.PENDING_CONFIRMATION.value
        appt_repo.update_appointment(db, draft)
        
        # Reset client state to exit flow
        client_repo.update_client_state(db, client, ConversationState.IDLE)
        
        return (
            f"Pronto, {draft.tutor_name}! Recebemos sua *solicitação* de {draft.service_type} "
            f"para o(a) {draft.pet_name} em {draft.preferred_date} ({draft.preferred_time}).\n\n"
            "⚠️ *Atenção:* Um atendente entrará em contato em breve para confirmar o horário exato!"
        )
        
    return "Estado desconhecido."
