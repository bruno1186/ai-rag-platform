"""Pipeline de RAG.

Suporta dois backends selecionados por configuracao:
- demo_mode=True  -> store em memoria + embeddings locais (sem credenciais).
- demo_mode=False -> OpenAI (embeddings/LLM) + Qdrant como vector store.
"""
from __future__ import annotations

from app.config import get_settings

SYSTEM_PROMPT = (
    "Voce e um assistente que responde SOMENTE com base no contexto fornecido. "
    "Se a resposta nao estiver no contexto, diga que nao sabe."
)


def _split(text: str, chunk_size: int, overlap: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


class RagPipeline:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.demo = self.settings.demo_mode
        if self.demo:
            from app.rag.demo_backend import InMemoryVectorStore
            self.store = InMemoryVectorStore()
        else:
            from langchain_openai import ChatOpenAI, OpenAIEmbeddings
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            from app.vectorstore.store import VectorStore

            embeddings = OpenAIEmbeddings(model=self.settings.embedding_model)
            self.llm = ChatOpenAI(model=self.settings.llm_model, temperature=0)
            self.store = VectorStore(embeddings)
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.settings.chunk_size,
                chunk_overlap=self.settings.chunk_overlap,
            )

    def ingest(self, text: str, metadata: dict | None = None) -> int:
        meta = metadata or {}
        if self.demo:
            chunks = _split(text, self.settings.chunk_size, self.settings.chunk_overlap)
            return self.store.add_texts(chunks, meta)
        chunks = self.splitter.split_text(text)
        self.store.add_texts(chunks, meta)
        return len(chunks)

    def query(self, question: str) -> dict:
        k = self.settings.top_k
        if self.demo:
            from app.rag.demo_backend import compose_answer

            hits = self.store.similarity_search(question, k)
            answer = compose_answer(question, [h.text for h in hits])
            return {"answer": answer, "sources": [h.metadata for h in hits]}

        docs = self.store.similarity_search(question, k=k)
        context = "\n\n".join(d.page_content for d in docs)
        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", f"Contexto:\n{context}\n\nPergunta: {question}"),
        ]
        answer = self.llm.invoke(messages).content
        return {"answer": answer, "sources": [d.metadata for d in docs]}
"""Pipeline de RAG: ingestao, retrieval e generation."""
from __future__ import annotations

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings
from app.vectorstore.store import VectorStore

SYSTEM_PROMPT = (
    "Voce e um assistente que responde SOMENTE com base no contexto fornecido. "
    "Se a resposta nao estiver no contexto, diga que nao sabe."
)


class RagPipeline:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.embeddings = OpenAIEmbeddings(model=settings.embedding_model)
        self.llm = ChatOpenAI(model=settings.llm_model, temperature=0)
        self.store = VectorStore(self.embeddings)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def ingest(self, text: str, metadata: dict | None = None) -> int:
        chunks = self.splitter.split_text(text)
        self.store.add_texts(chunks, metadata or {})
        return len(chunks)

    def query(self, question: str) -> dict:
        docs = self.store.similarity_search(question, k=self.settings.top_k)
        context = "\n\n".join(d.page_content for d in docs)
        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", f"Contexto:\n{context}\n\nPergunta: {question}"),
        ]
        answer = self.llm.invoke(messages).content
        return {
            "answer": answer,
            "sources": [d.metadata for d in docs],
        }
