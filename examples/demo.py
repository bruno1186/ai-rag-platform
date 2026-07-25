"""Demonstracao ponta a ponta do pipeline de RAG em demo_mode.

Roda sem OpenAI e sem Qdrant:

    python -m examples.demo
"""
from app.rag.pipeline import RagPipeline

DOCUMENTOS = [
    (
        "O plano Enterprise inclui SSO via SAML, logs de auditoria com retencao "
        "de 12 meses e SLA de 99.9%. O suporte e prioritario com resposta em ate 1 hora.",
        {"fonte": "plano-enterprise"},
    ),
    (
        "O plano Starter e gratuito, permite ate 3 usuarios e nao inclui SSO. "
        "O suporte e feito por email com resposta em ate 48 horas.",
        {"fonte": "plano-starter"},
    ),
]

PERGUNTAS = [
    "Qual plano oferece SSO e qual o SLA?",
    "Quantos usuarios o plano gratuito permite?",
]


def main() -> None:
    pipeline = RagPipeline()
    for texto, meta in DOCUMENTOS:
        n = pipeline.ingest(texto, meta)
        print(f"ingerido: {meta['fonte']} ({n} chunk(s))")

    print("-" * 60)
    for pergunta in PERGUNTAS:
        resultado = pipeline.query(pergunta)
        print(f"P: {pergunta}")
        print(f"R: {resultado['answer']}")
        print(f"fontes: {[s.get('fonte') for s in resultado['sources']]}")
        print("-" * 60)


if __name__ == "__main__":
    main()
