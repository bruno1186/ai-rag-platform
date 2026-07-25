"""Abstracao do banco vetorial usando Qdrant via LangChain."""
from __future__ import annotations

import uuid

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import get_settings


class VectorStore:
    def __init__(self, embeddings) -> None:
        settings = get_settings()
        self.client = QdrantClient(url=settings.qdrant_url)
        self.collection = settings.collection_name
        self._ensure_collection(embeddings)
        self.store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection,
            embedding=embeddings,
        )

    def _ensure_collection(self, embeddings) -> None:
        existing = {c.name for c in self.client.get_collections().collections}
        if self.collection not in existing:
            dim = len(embeddings.embed_query("dimension probe"))
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def add_texts(self, texts: list[str], metadata: dict) -> list[str]:
        docs = [Document(page_content=t, metadata=metadata) for t in texts]
        ids = [str(uuid.uuid4()) for _ in docs]
        self.store.add_documents(docs, ids=ids)
        return ids

    def similarity_search(self, query: str, k: int = 4) -> list[Document]:
        return self.store.similarity_search(query, k=k)
