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
