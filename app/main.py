"""API FastAPI expondo o pipeline de RAG."""
from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.pipeline import RagPipeline

app = FastAPI(title="ai-rag-platform", version="1.0.0")
pipeline = RagPipeline()


class IngestRequest(BaseModel):
    text: str
    metadata: dict | None = None


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ingest")
def ingest(req: IngestRequest) -> dict:
    chunks = pipeline.ingest(req.text, req.metadata)
    return {"ingested_chunks": chunks}


@app.post("/query")
def query(req: QueryRequest) -> dict:
    return pipeline.query(req.question)
