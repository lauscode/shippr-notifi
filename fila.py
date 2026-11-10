from database import (
    atualizar_status,
    buscar_pendentes,
    incrementar_tentativas,
)


def obter_pendentes(limite=10):
    return buscar_pendentes(limite)


def marcar_processando(id_banco):
    atualizar_status(
        id_banco,
        "processando",
    )


def marcar_notificada(id_banco):
    incrementar_tentativas(id_banco)

    atualizar_status(
        id_banco,
        "notificada",
    )


def marcar_erro(
    id_banco,
    mensagem_erro,
):
    incrementar_tentativas(id_banco)

    atualizar_status(
        id_banco,
        "erro",
        mensagem_erro,
    )