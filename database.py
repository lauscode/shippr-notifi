import sqlite3
from datetime import datetime, timezone


BANCO = "notificacoes.db"


def conectar():
    return sqlite3.connect(BANCO)


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_notificacao INTEGER NOT NULL UNIQUE,
            romaneio_id INTEGER,
            parada_id INTEGER,
            entregador_id INTEGER,
            titulo TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            tipo TEXT,
            api TEXT,
            contato TEXT,
            status TEXT NOT NULL DEFAULT 'pendente',
            tentativas INTEGER NOT NULL DEFAULT 0,
            erro TEXT,
            criado_em TEXT NOT NULL,
            processado_em TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_notificacoes_status
        ON notificacoes(status)
        """
    )

    conexao.commit()
    conexao.close()


def salvar_notificacao(dados):
    conexao = conectar()
    cursor = conexao.cursor()

    criado_em = datetime.now(
        timezone.utc
    ).isoformat()

    cursor.execute(
        """
        INSERT INTO notificacoes (
            id_notificacao,
            romaneio_id,
            parada_id,
            entregador_id,
            titulo,
            mensagem,
            tipo,
            api,
            contato,
            status,
            tentativas,
            criado_em
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dados["id_notificacao"],
            dados.get("romaneio_id"),
            dados.get("parada_id"),
            dados.get("entregador_id"),
            dados["titulo"],
            dados["mensagem"],
            dados["dados"].get("tipo"),
            dados["dados"].get("api"),
            dados["dados"].get("contato"),
            "pendente",
            0,
            criado_em,
        ),
    )

    conexao.commit()

    id_banco = cursor.lastrowid

    conexao.close()

    return {
        "id": id_banco,
        "id_notificacao": dados[
            "id_notificacao"
        ],
        "status": "pendente",
        "criado_em": criado_em,
    }


def buscar_pendentes(limite=10):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            id_notificacao,
            romaneio_id,
            parada_id,
            entregador_id,
            titulo,
            mensagem,
            tipo,
            api,
            contato,
            status,
            tentativas,
            erro,
            criado_em,
            processado_em
        FROM notificacoes
        WHERE status = 'pendente'
        ORDER BY id
        LIMIT ?
        """,
        (limite,),
    )

    linhas = cursor.fetchall()

    conexao.close()

    notificacoes = []

    for linha in linhas:
        notificacoes.append(
            {
                "id": linha[0],
                "id_notificacao": linha[1],
                "romaneio_id": linha[2],
                "parada_id": linha[3],
                "entregador_id": linha[4],
                "titulo": linha[5],
                "mensagem": linha[6],
                "tipo": linha[7],
                "api": linha[8],
                "contato": linha[9],
                "status": linha[10],
                "tentativas": linha[11],
                "erro": linha[12],
                "criado_em": linha[13],
                "processado_em": linha[14],
            }
        )

    return notificacoes


def listar_notificacoes(limite=50):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            id_notificacao,
            romaneio_id,
            parada_id,
            entregador_id,
            titulo,
            mensagem,
            tipo,
            api,
            contato,
            status,
            tentativas,
            erro,
            criado_em,
            processado_em
        FROM notificacoes
        ORDER BY id DESC
        LIMIT ?
        """,
        (limite,),
    )

    linhas = cursor.fetchall()

    conexao.close()

    notificacoes = []

    for linha in linhas:
        notificacoes.append(
            {
                "id": linha[0],
                "id_notificacao": linha[1],
                "romaneio_id": linha[2],
                "parada_id": linha[3],
                "entregador_id": linha[4],
                "titulo": linha[5],
                "mensagem": linha[6],
                "tipo": linha[7],
                "api": linha[8],
                "contato": linha[9],
                "status": linha[10],
                "tentativas": linha[11],
                "erro": linha[12],
                "criado_em": linha[13],
                "processado_em": linha[14],
            }
        )

    return notificacoes


def atualizar_status(
    id_banco,
    status,
    erro=None,
):
    conexao = conectar()
    cursor = conexao.cursor()

    processado_em = None

    if status in (
        "notificada",
        "erro",
    ):
        processado_em = datetime.now(
            timezone.utc
        ).isoformat()

    cursor.execute(
        """
        UPDATE notificacoes
        SET
            status = ?,
            erro = ?,
            processado_em = ?
        WHERE id = ?
        """,
        (
            status,
            erro,
            processado_em,
            id_banco,
        ),
    )

    conexao.commit()
    conexao.close()


def incrementar_tentativas(id_banco):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE notificacoes
        SET tentativas = tentativas + 1
        WHERE id = ?
        """,
        (id_banco,),
    )

    conexao.commit()
    conexao.close()


def buscar_notificacao(
    id_notificacao,
):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            id_notificacao,
            romaneio_id,
            parada_id,
            entregador_id,
            titulo,
            mensagem,
            tipo,
            api,
            contato,
            status,
            tentativas,
            erro,
            criado_em,
            processado_em
        FROM notificacoes
        WHERE id_notificacao = ?
        """,
        (id_notificacao,),
    )

    linha = cursor.fetchone()

    conexao.close()

    if linha is None:
        return None

    return {
        "id": linha[0],
        "id_notificacao": linha[1],
        "romaneio_id": linha[2],
        "parada_id": linha[3],
        "entregador_id": linha[4],
        "titulo": linha[5],
        "mensagem": linha[6],
        "tipo": linha[7],
        "api": linha[8],
        "contato": linha[9],
        "status": linha[10],
        "tentativas": linha[11],
        "erro": linha[12],
        "criado_em": linha[13],
        "processado_em": linha[14],
    }


criar_tabelas()
