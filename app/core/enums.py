from enum import Enum

class ConversationState(str, Enum):
    # Graphic Print Shop States
    INICIO = "inicio"
    ORCAMENTO = "orcamento"
    COLETA_PRODUTO = "coleta_produto"
    COLETA_TAMANHO = "coleta_tamanho"
    COLETA_QUANTIDADE = "coleta_quantidade"
    CONFIRMACAO = "confirmacao"
    DUVIDAS = "duvidas"
    DUVIDA_PRAZO = "duvida_prazo"
    DUVIDA_MATERIAL = "duvida_material"
    DUVIDA_ARQUIVO = "duvida_arquivo"
    ENCAMINHAMENTO = "encaminhamento"
    FINAL = "final"
