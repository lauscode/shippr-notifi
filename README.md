# Shippr Notifi

Serviço de notificações da Shippr responsável por receber eventos relacionados a rotas, trechos e paradas, armazenar as notificações em uma fila e processá-las automaticamente.

## Funcionalidades

- Recebimento de notificações via JSON
- Armazenamento das notificações em SQLite
- Processamento automático por worker
- Controle de status da notificação
- Controle de tentativas de envio
- Proteção contra notificações duplicadas
- Consulta do histórico de notificações
- Integração com o módulo `shippr-route`
- Suporte preparado para notificações via RCS

## Fluxo

O serviço funciona da seguinte forma:

1. O `shippr-route` gera um evento.
2. O evento é enviado para o `shippr-notifi`.
3. A notificação é salva com status `pendente`.
4. O worker busca notificações pendentes.
5. A notificação é processada.
6. O status é atualizado para `notificada` ou `erro`.

## Tipos de eventos

Atualmente são utilizados eventos como:

- `notifica_rota`
- `notifica_trecho`
- `notifica_parada_entregue`
- `notifica_entrega`

## Exemplo de JSON

```json
{
  "id_notificacao": 123,
  "romaneio_id": 456,
  "parada_id": 654,
  "entregador_id": 123,
  "titulo": "Entregador saiu com sua entrega.",
  "mensagem": "A sua entrega será a próxima.",
  "dados": {
    "tipo": "notifica_entrega",
    "api": "RCS",
    "contato": "41999860191"
  }
}
```

## Tecnologias

- Python
- FastAPI
- SQLite
- Uvicorn
- Requests

## Instalação

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando a API

No PowerShell:

```powershell
& ".\.venv\Scripts\python.exe" -m uvicorn api:app --reload --port 8002
```

Swagger:

```text
http://127.0.0.1:8002/docs
```

## Executando o Worker

Em outro terminal:

```powershell
& ".\.venv\Scripts\python.exe" worker.py
```

O worker verifica periodicamente as notificações pendentes e realiza o processamento.

## Endpoints principais

### Criar notificação

```text
POST /notificacoes
```

### Listar notificações

```text
GET /notificacoes
```

### Buscar notificação

```text
GET /notificacoes/{id_notificacao}
```

### Processar fila manualmente

```text
POST /fila/processar
```

## Status possíveis

- `pendente`
- `processando`
- `notificada`
- `erro`

## Integração

O projeto é integrado ao:

```text
shippr-route
```

Eventos de início de rota, início de trecho e conclusão de parada podem gerar notificações automaticamente.

## Observação

O processamento RCS está atualmente preparado/simulado no projeto. Para envio real será necessário configurar o provedor e as credenciais da API de RCS utilizadas pela Shippr.