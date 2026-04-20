from app.utils.text_parser import clean_text
from app.services.response_builder import (
    build_prices_message, build_address, build_hours, build_greeting
)

def route_intent(message: str) -> str | None:
    """
    Roteia a mensagem por palavras chaves. 
    Retorna a string formatada ou None (se não for intent stateless ou for fallback).
    """
    cleaned = clean_text(message)
    
    # Consultations
    if any(k in cleaned for k in ["consulta", "veterinario", "medico"]):
        return build_prices_message("consultas")
        
    # Vaccines
    if any(k in cleaned for k in ["vacina", "v10", "raiva", "giardia"]):
        return build_prices_message("vacinas")
        
    # Exams
    if any(k in cleaned for k in ["exame", "sangue", "ultrassom", "raio-x", "raiox", "fezes"]):
        return build_prices_message("exames")
        
    # Info
    if any(k in cleaned for k in ["horario", "funcionamento", "aberto", "horas"]):
        return build_hours()
        
    if any(k in cleaned for k in ["endereco", "local", "onde", "rua"]):
        return build_address()
        
    # Scheduling starter is handled in the message_handler or we return None here
    if any(k in cleaned for k in ["agendar", "marcar", "agendamento"]):
        return "START_SCHEDULING"
        
    return build_greeting()
