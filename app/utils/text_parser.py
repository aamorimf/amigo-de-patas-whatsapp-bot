import re
import unicodedata

def clean_text(text: str) -> str:
    """Removes accents and converts to lowercase."""
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return text

def is_valid_service_type(text: str) -> bool:
    """Validates if the user wants one of the 3 services."""
    cleaned = clean_text(text)
    keywords = ["consulta", "vacina", "exame"]
    return any(keyword in cleaned for keyword in keywords)

def is_valid_date(text: str) -> bool:
    """
    Validates simple dates:
    hoje, amanha, dias da semana, ou padroes numéricos como 15/04, 15/04/2026
    """
    cleaned = clean_text(text)
    
    # Block vague words
    vague_words = ["sim", "ok", "qualquer", "tanto faz", "nao sei", "decidir"]
    if any(v in cleaned for v in vague_words):
        return False
        
    pattern = r'^(hoje|amanha|segunda|terca|quarta|quinta|sexta|sabado|domingo|\d{1,2}/\d{1,2}(/\d{2,4})?)$'
    return bool(re.search(pattern, cleaned))

def is_valid_time(text: str) -> bool:
    """
    Validates time:
    15h, 15:30, manha, tarde.
    """
    cleaned = clean_text(text)
    
    # Block vague words
    vague_words = ["qualquer", "depois", "tanto faz", "nao sei"]
    if any(v in cleaned for v in vague_words):
        return False
        
    pattern = r'^(\d{1,2}(h|:\d{2})?|manha|tarde|noite)$'
    return bool(re.search(pattern, cleaned))
