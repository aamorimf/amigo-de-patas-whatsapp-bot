from sqlalchemy.orm import Session
from app.models.schema import Client
from app.core.enums import ConversationState
from app.repositories import client_repository as client_repo
from app.repositories import quote_repository as quote_repo
from app.core.state_config import STATE_CONFIG

def format_message(message: str, quote) -> str:
    if not quote:
        return message
    produto = quote.produto or "Não informado"
    tamanho = quote.tamanho or "Não informado"
    quantidade = quote.quantidade or "Não informado"
    return message.format(produto=produto, tamanho=tamanho, quantidade=quantidade)

def process_state_machine(db: Session, client: Client, message: str) -> str:
    current_state = client.current_state
    
    if current_state not in STATE_CONFIG or current_state == "IDLE":
        # Se estiver fora do fluxo gráfico ou em IDLE, vai para o inicio
        current_state = "inicio"
        client_repo.update_client_state(db, client, ConversationState.INICIO)
    
    config = STATE_CONFIG[current_state]
    quote = quote_repo.get_or_create_quote(db, client.id)
    
    next_state = None
    action_to_run = None
    is_fallback = False
    
    text = message.strip()
    
    if config.get("type") == "menu":
        options = config.get("options", {})
        if text in options:
            selected_option = options[text]
            next_state = selected_option.get("next")
            action_to_run = selected_option.get("action")
        else:
            is_fallback = True
            
    elif config.get("type") == "input":
        if not text:
            is_fallback = True
        else:
            next_state = config.get("next")
            action_cfg = config.get("action")
            if action_cfg:
                action_to_run = {"field": action_cfg.get("field"), "value": text}
            
    if is_fallback:
        # Fallback: não muda estado, retorna msg de erro + msg do estado atual
        error_msg = STATE_CONFIG["erro"]["message"]
        state_msg = format_message(config["message"], quote)
        return error_msg + state_msg

    # Execute action se existir
    if action_to_run:
        field = action_to_run.get("field")
        val = action_to_run.get("value")
        if field:
            quote_repo.update_quote_field(db, quote, field, val)
            
    # Altera estado para o próximo
    if next_state:
        # Se entrou em orçamento, reseta o quote
        if next_state == "orcamento":
            quote = quote_repo.reset_quote(db, client.id)
            
        client_repo.update_client_state(db, client, ConversationState(next_state))
        
        # Pega a config do proximo estado para retornar a mensagem
        next_config = STATE_CONFIG[next_state]
        
        # Se for um redirect direto como encaminhamento -> final
        if next_config.get("type") == "redirect":
            redirect_msg = format_message(next_config["message"], quote)
            final_target = next_config.get("next")
            client_repo.update_client_state(db, client, ConversationState(final_target))
            final_config = STATE_CONFIG[final_target]
            final_msg = format_message(final_config["message"], quote)
            return redirect_msg + "\n\n" + final_msg
            
        return format_message(next_config["message"], quote)

    # Fallback seguro caso algo falhe na configuração
    return format_message(config["message"], quote)
