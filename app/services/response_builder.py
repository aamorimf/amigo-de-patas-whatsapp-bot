from app.core.constants import CLINIC_INFO, SERVICES_CATALOG

def build_prices_message(service_category: str) -> str:
    if service_category not in SERVICES_CATALOG:
        return "Serviço não encontrado."
    
    msg = f"Tabela de preços para {service_category.capitalize()}:\n\n"
    for key, item in SERVICES_CATALOG[service_category].items():
        msg += f"- {item['name']}: R${item['price']}\n"
    return msg

def build_greeting() -> str:
    return (
        "Olá! Sou o assistente virtual da Clínica Amigo de Patas 🐾\n\n"
        "Como posso ajudar hoje? Você pode me perguntar sobre:\n"
        "- Preços de Consultas, Vacinas ou Exames\n"
        "- Nossos Horários e Endereço\n"
        "- Ou simplesmente digite 'Agendar' para marcar uma visita!"
    )

def build_address() -> str:
    return f"Nosso endereço é:\n📍 {CLINIC_INFO['address']}"

def build_hours() -> str:
    return f"Nossos horários de funcionamento:\n🕒\n{CLINIC_INFO['hours']}"
