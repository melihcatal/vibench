import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: Optional[str]
    model: str


def get_embeddings_config(model: Optional[str] = None) -> EmbeddingsConfig:
    return EmbeddingsConfig(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model=model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    )


def get_embeddings_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))


def get_embeddings_client_and_model(model: Optional[str] = None, api_key: Optional[str] = None):
    config = get_embeddings_config(model=model)
    client = get_embeddings_client(api_key=api_key or config.api_key)
    return client, config.model
