from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracoes da aplicacao, carregadas de variaveis de ambiente / .env."""

    # Em demo_mode a plataforma roda sem OpenAI/Qdrant, usando um backend
    # local (embeddings deterministicos + store em memoria). Util para
    # avaliar o fluxo de RAG de ponta a ponta sem credenciais.
    demo_mode: bool = True

    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"

    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "documents"

    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracoes da aplicacao, carregadas de variaveis de ambiente / .env."""

    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"

    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "documents"

    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
