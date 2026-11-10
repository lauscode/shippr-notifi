def enviar_notificacao(notificacao):
    api = notificacao.get("api")

    if api == "RCS":
        return enviar_rcs(notificacao)

    return {
        "status": "erro",
        "mensagem": f"API de notificação não suportada: {api}",
    }


def enviar_rcs(notificacao):
    contatos = notificacao.get("contato", "")

    lista_contatos = [
        contato.strip()
        for contato in contatos.split(",")
        if contato.strip()
    ]

    if not lista_contatos:
        return {
            "status": "erro",
            "mensagem": "Nenhum contato informado.",
        }

    return {
        "status": "sucesso",
        "api": "RCS",
        "contatos": lista_contatos,
        "titulo": notificacao.get("titulo"),
        "mensagem": notificacao.get("mensagem"),
    }