"""Backend local para demo_mode: embeddings deterministicos e store em memoria.

Nao depende de OpenAI nem de Qdrant. Serve para validar o fluxo de RAG
ponta a ponta (chunking -> embedding -> retrieval -> geracao) sem credenciais.
Nao deve ser usado em producao: a qualidade semantica e limitada de proposito.
"""
from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field

_DIM = 256
_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def embed(text: str) -> list[float]:
    """Embedding bag-of-words com hashing. Deterministico e sem dependencias."""
    vec = [0.0] * _DIM
    for token in _tokens(text):
        h = int(hashlib.md5(token.encode()).hexdigest(), 16)
        vec[h % _DIM] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


@dataclass
class Record:
    text: str
    metadata: dict
    vector: list[float]


@dataclass
class InMemoryVectorStore:
    records: list[Record] = field(default_factory=list)

    def add_texts(self, texts: list[str], metadata: dict) -> int:
        for text in texts:
            self.records.append(Record(text, metadata, embed(text)))
        return len(texts)

    def similarity_search(self, query: str, k: int) -> list[Record]:
        qv = embed(query)
        ranked = sorted(self.records, key=lambda r: cosine(qv, r.vector), reverse=True)
        return ranked[:k]


def compose_answer(question: str, contexts: list[str]) -> str:
    """Resposta extrativa simples: sem LLM, apenas realca o trecho recuperado."""
    if not contexts:
        return "Nao sei responder: nenhum contexto relevante foi encontrado."
    return (
        "Com base no contexto recuperado:\n"
        + contexts[0].strip()
    )
