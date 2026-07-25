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
