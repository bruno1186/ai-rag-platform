# ai-rag-platform

Plataforma de RAG (Retrieval-Augmented Generation) em Python + FastAPI. Expoe ingestao de documentos, busca semantica em vector store e geracao aumentada por LLM, com um servidor MCP (Model Context Protocol) para disponibilizar tools e contexto a assistentes.

## Modos de execucao

A plataforma tem dois backends selecionados por configuracao (`DEMO_MODE`):

- `DEMO_MODE=true` (padrao): roda sem credenciais, usando embeddings deterministicos e vector store em memoria. Serve para avaliar o fluxo completo de RAG localmente.
- `DEMO_MODE=false`: usa OpenAI para embeddings/LLM e Qdrant como vector store.

## Stack

- Python 3.11+, FastAPI, Pydantic v2
- LangChain (orquestracao no modo produtivo)
- OpenAI (LLM e embeddings) e Qdrant (vector store) quando `DEMO_MODE=false`
- MCP (Model Context Protocol)
- Docker e docker-compose

## Estrutura

```
app/
  main.py            # bootstrap FastAPI (init preguicoso do pipeline)
  config.py          # settings via Pydantic
  rag/
    pipeline.py      # orquestracao: ingest / query
    demo_backend.py  # embeddings + store em memoria (DEMO_MODE)
  vectorstore/
    store.py         # adapter Qdrant (modo produtivo)
  mcp/
    server.py        # servidor MCP
examples/
  demo.py            # demonstracao ponta a ponta em memoria
requirements.txt
docker-compose.yml
```

## Rodando a demo (sem credenciais)

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m examples.demo
```

## Rodando a API

```
uvicorn app.main:app --reload
```

API em `http://localhost:8000`, docs em `http://localhost:8000/docs`.

Endpoints: `POST /ingest`, `POST /query`, `GET /health`.

## Modo produtivo

Defina `DEMO_MODE=false` e configure `OPENAI_API_KEY` e `QDRANT_URL` no `.env`, depois suba o Qdrant:

```
docker-compose up -d
uvicorn app.main:app --reload
```

## Seguranca

Nunca faca commit da `OPENAI_API_KEY` ou outras credenciais. Use `.env` (ignorado pelo git).

## Licenca

MIT
