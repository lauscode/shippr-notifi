import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from database import (
    buscar_notificacao,
    criar_tabelas,
    listar_notificacoes,
    salvar_notificacao,
)
from worker import processar_fila


app = FastAPI(
    title="Shippr Notifi",
    version="1.0.0",
)


class DadosNotificacao(BaseModel):
    tipo: str
    api: str
    contato: str


class NotificacaoEntrada(BaseModel):
    id_notificacao: int
    romaneio_id: Optional[int] = None
    parada_id: Optional[int] = None
    entregador_id: Optional[int] = None
    titulo: str = Field(
        min_length=1
    )
    mensagem: str = Field(
        min_length=1
    )
    dados: DadosNotificacao


@app.on_event("startup")
def startup():
    criar_tabelas()


@app.get("/")
def raiz():
    return {
        "status": "online",
        "servico": "shippr-notifi",
    }


@app.post(
    "/notificacoes",
    status_code=status.HTTP_201_CREATED,
)
def criar_notificacao(
    dados: NotificacaoEntrada,
):
    existente = buscar_notificacao(
        dados.id_notificacao
    )

    if existente is not None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Já existe uma notificação com "
                "esse id_notificacao."
            ),
        )

    try:
        resultado = salvar_notificacao(
            dados.model_dump()
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=(
                "Já existe uma notificação com "
                "esse id_notificacao."
            ),
        )

    return {
        "status": "recebida",
        "mensagem": (
            "Notificação adicionada à fila."
        ),
        "notificacao": resultado,
    }


@app.get(
    "/notificacoes"
)
def listar(
    limite: int = 50,
):
    if limite < 1:
        raise HTTPException(
            status_code=422,
            detail=(
                "O limite deve ser maior "
                "que zero."
            ),
        )

    if limite > 200:
        limite = 200

    return {
        "quantidade": len(
            listar_notificacoes(
                limite
            )
        ),
        "notificacoes": (
            listar_notificacoes(
                limite
            )
        ),
    }


@app.get(
    "/notificacoes/{id_notificacao}"
)
def consultar_notificacao(
    id_notificacao: int,
):
    notificacao = buscar_notificacao(
        id_notificacao
    )

    if notificacao is None:
        raise HTTPException(
            status_code=404,
            detail="Notificação não encontrada.",
        )

    return notificacao


@app.post(
    "/fila/processar"
)
def processar():
    return processar_fila()