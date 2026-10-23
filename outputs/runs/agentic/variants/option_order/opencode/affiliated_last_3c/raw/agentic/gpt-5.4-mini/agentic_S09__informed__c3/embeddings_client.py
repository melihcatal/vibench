import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class EmbeddingsConfig:
    model: str
    dimension: int | None


def load_embeddings_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        dimension=int(os.getenv("OPENAI_EMBEDDING_DIMENSION", "0")) or None,
    )


def get_embeddings_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
