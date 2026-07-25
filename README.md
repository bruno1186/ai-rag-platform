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
# ai-rag-platform

Plataforma de IA com **RAG (Retrieval-Augmented Generation)** construida em Python + FastAPI. Integra embeddings, banco vetorial, orquestracao com LangChain e um servidor **MCP (Model Context Protocol)** para expor ferramentas e contexto a assistentes de IA.

## Visao geral

O objetivo e servir de base moderna para aplicacoes de IA em producao: ingestao de documentos, geracao de embeddings, busca semantica em vector store, montagem de contexto e resposta aumentada por um LLM, com observabilidade e protocolos padronizados.

## Tecnologias e protocolos

- Python 3.11+
- FastAPI (API HTTP e streaming)
- LangChain (orquestracao de RAG)
- OpenAI / modelos compativeis (LLM e embeddings)
- Qdrant / pgvector (banco vetorial)
- MCP - Model Context Protocol (servidor de tools/resources)
- Pydantic v2 (validacao e settings)
- Docker e docker-compose

## Arquitetura RAG

1. **Ingestao**: documentos sao divididos em chunks.
2. **Embeddings**: cada chunk vira um vetor.
3. **Indexacao**: os vetores sao gravados no vector store.
4. **Retrieval**: a pergunta do usuario e vetorizada e busca os chunks mais relevantes.
5. **Augmentation**: os chunks recuperados compoem o contexto do prompt.
6. **Generation**: o LLM responde com base no contexto recuperado, reduzindo alucinacoes.

## Estrutura de pastas

```
ai-rag-platform/
  app/
    api/            # rotas FastAPI
    rag/            # pipeline de RAG (ingest, retrieve, generate)
    embeddings/     # geracao de embeddings
    vectorstore/    # abstracao do banco vetorial
    mcp/            # servidor MCP (tools e resources)
    config.py       # settings via Pydantic
    main.py         # bootstrap da aplicacao
  tests/
  requirements.txt
  docker-compose.yml
  .env.example
```

## Como rodar localmente

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha sua OPENAI_API_KEY
docker-compose up -d   # sobe o Qdrant
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000` e a documentacao em `http://localhost:8000/docs`.

## Endpoints principais

- `POST /ingest` - ingere um documento no vector store
- `POST /query` - faz uma pergunta com RAG
- `GET /health` - healthcheck

## Seguranca

Nunca faca commit da `OPENAI_API_KEY` ou outras credenciais. Use `.env` (ignorado pelo git).

## Licenca

MIT
# ai-rag-platform
Plataforma de IA com RAG (retrieval-augmented generation) em Python + FastAPI, vector database, embeddings, LangChain e servidor MCP (Model Context Protocol).
