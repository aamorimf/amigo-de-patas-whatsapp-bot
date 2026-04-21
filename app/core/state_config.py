STATE_CONFIG = {
    "inicio": {
        "type": "menu",
        "message": (
            "Olá! Seja bem-vindo 👋\n"
            "Sou o assistente virtual da gráfica.\n\n"
            "Posso te ajudar com orçamento, dúvidas ou atendimento.\n\n"
            "Escolha uma opção:\n"
            "1️⃣ Fazer um orçamento\n"
            "2️⃣ Tirar dúvidas\n"
            "3️⃣ Falar com atendente"
        ),
        "options": {
            "1": {"next": "orcamento"},
            "2": {"next": "duvidas"},
            "3": {"next": "encaminhamento"}
        }
    },
    "orcamento": {
        "type": "menu",
        "message": (
            "Perfeito! Sobre qual tipo de produto você deseja orçamento?\n\n"
            "1️⃣ Offset (Cartões, Panfletos)\n"
            "2️⃣ Comunicação Visual (Lonas, Adesivos)\n"
            "3️⃣ Sublimação (Brindes)"
        ),
        "options": {
            "1": {"next": "coleta_produto", "action": {"field": "setor", "value": "offset"}},
            "2": {"next": "coleta_produto", "action": {"field": "setor", "value": "sign"}},
            "3": {"next": "coleta_produto", "action": {"field": "setor", "value": "sublimacao"}}
        }
    },
    "coleta_produto": {
        "type": "input",
        "message": "Qual produto você precisa?",
        "action": {"field": "produto"},
        "next": "coleta_tamanho"
    },
    "coleta_tamanho": {
        "type": "input",
        "message": "Qual o tamanho?",
        "action": {"field": "tamanho"},
        "next": "coleta_quantidade"
    },
    "coleta_quantidade": {
        "type": "input",
        "message": "Qual a quantidade?",
        "action": {"field": "quantidade"},
        "next": "confirmacao"
    },
    "confirmacao": {
        "type": "menu",
        "message": (
            "Perfeito! Só confirmando suas informações:\n\n"
            "Produto: {produto}\n"
            "Tamanho: {tamanho}\n"
            "Quantidade: {quantidade}\n\n"
            "Está correto?\n\n"
            "1️⃣ Sim\n"
            "2️⃣ Corrigir"
        ),
        "options": {
            "1": {"next": "encaminhamento"},
            "2": {"next": "coleta_produto"}
        }
    },
    "duvidas": {
        "type": "menu",
        "message": (
            "Sem problemas, sobre o que é sua dúvida?\n\n"
            "1️⃣ Prazo de produção\n"
            "2️⃣ Tipo de material\n"
            "3️⃣ Envio de arquivo"
        ),
        "options": {
            "1": {"next": "duvida_prazo"},
            "2": {"next": "duvida_material"},
            "3": {"next": "duvida_arquivo"}
        }
    },
    "duvida_prazo": {
        "type": "menu",
        "message": (
            "O prazo de produção varia conforme o produto, mas geralmente fica entre 1 e 3 dias.\n\n"
            "Deseja fazer um orçamento ou falar com atendente?\n\n"
            "1️⃣ Fazer orçamento\n"
            "2️⃣ Falar com atendente"
        ),
        "options": {
            "1": {"next": "orcamento"},
            "2": {"next": "encaminhamento"}
        }
    },
    "duvida_material": {
        "type": "menu",
        "message": (
            "Trabalhamos com diversos tipos de materiais, dependendo do produto.\n\n"
            "Se quiser, posso te ajudar com um orçamento ou te encaminhar para um atendente.\n\n"
            "1️⃣ Fazer orçamento\n"
            "2️⃣ Falar com atendente"
        ),
        "options": {
            "1": {"next": "orcamento"},
            "2": {"next": "encaminhamento"}
        }
    },
    "duvida_arquivo": {
        "type": "menu",
        "message": (
            "Você pode enviar seu arquivo em PDF ou imagem com boa qualidade.\n\n"
            "Se precisar, posso te ajudar com orçamento ou encaminhar para um atendente.\n\n"
            "1️⃣ Fazer orçamento\n"
            "2️⃣ Falar com atendente"
        ),
        "options": {
            "1": {"next": "orcamento"},
            "2": {"next": "encaminhamento"}
        }
    },
    "encaminhamento": {
        "type": "redirect",
        "message": "Perfeito! Já anotei suas informações 👍\nVou encaminhar seu atendimento para um atendente 👍",
        "next": "final"
    },
    "final": {
        "type": "menu",
        "message": (
            "Seu atendimento foi encaminhado 👍\n\n"
            "Se precisar de mais alguma coisa, posso te ajudar também:\n\n"
            "1️⃣ Novo orçamento\n"
            "2️⃣ Tirar outra dúvida\n"
            "3️⃣ Falar com atendente"
        ),
        "options": {
            "1": {"next": "orcamento"},
            "2": {"next": "duvidas"},
            "3": {"next": "encaminhamento"}
        }
    },
    "erro": {
        "message": "Não entendi sua resposta 😅\n\nPor favor, escolha uma das opções abaixo digitando o número correspondente.\n\n"
    }
}
