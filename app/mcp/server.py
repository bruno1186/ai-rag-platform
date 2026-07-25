"""Servidor MCP (Model Context Protocol).

Expoe o pipeline de RAG como uma "tool" que qualquer cliente MCP
(ex: Claude Desktop, IDEs com suporte a MCP) pode invocar. Rode com:

    python -m app.mcp.server
"""
from mcp.server.fastmcp import FastMCP

from app.rag.pipeline import RagPipeline

mcp = FastMCP("ai-rag-platform")
pipeline = RagPipeline()


@mcp.tool()
def rag_query(question: str) -> str:
    """Responde a uma pergunta usando RAG sobre a base de conhecimento indexada."""
    result = pipeline.query(question)
    return result["answer"]


@mcp.tool()
def rag_ingest(text: str, source: str = "manual") -> str:
    """Ingere um novo documento na base de conhecimento vetorial."""
    chunks = pipeline.ingest(text, {"source": source})
    return f"Documento ingerido em {chunks} chunks."


if __name__ == "__main__":
    mcp.run()
