import time

from fila import (
    marcar_erro,
    marcar_notificada,
    marcar_processando,
    obter_pendentes,
)
from notificadores import enviar_notificacao


def processar_fila():
    notificacoes = obter_pendentes(
        limite=10
    )

    if not notificacoes:
        return {
            "status": "vazio",
            "processadas": 0,
        }

    processadas = 0

    for notificacao in notificacoes:
        id_banco = notificacao["id"]

        marcar_processando(
            id_banco
        )

        try:
            resultado = enviar_notificacao(
                notificacao
            )

            if (
                resultado.get("status")
                == "sucesso"
            ):
                marcar_notificada(
                    id_banco
                )

                processadas += 1

            else:
                marcar_erro(
                    id_banco,
                    resultado.get(
                        "mensagem",
                        "Erro desconhecido no envio.",
                    ),
                )

        except Exception as erro:
            marcar_erro(
                id_banco,
                str(erro),
            )

    return {
        "status": "sucesso",
        "processadas": processadas,
    }


def executar_worker(
    intervalo_segundos=5,
):
    print(
        "Worker de notificações iniciado."
    )

    while True:
        resultado = processar_fila()

        if resultado["status"] != "vazio":
            print(resultado)

        time.sleep(
            intervalo_segundos
        )


if __name__ == "__main__":
    executar_worker()