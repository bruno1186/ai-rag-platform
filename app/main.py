"""API FastAPI expondo o pipeline de RAG."""
from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseModel

from app.config import get_settings
from app.rag.pipeline import RagPipeline

app = FastAPI(title="ai-rag-platform", version="1.0.0")


@lru_cache
def get_pipeline() -> RagPipeline:
    # Inicializacao preguicosa: a app sobe mesmo sem backend pronto;
    # o pipeline so e construido no primeiro uso.
    return RagPipeline()


class IngestRequest(BaseModel):
    text: str
    metadata: dict | None = None


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "demo_mode": get_settings().demo_mode}


@app.post("/ingest")
def ingest(req: IngestRequest) -> dict:
    return {"ingested_chunks": get_pipeline().ingest(req.text, req.metadata)}


@app.post("/query")
def query(req: QueryRequest) -> dict:
    return get_pipeline().query(req.question)
