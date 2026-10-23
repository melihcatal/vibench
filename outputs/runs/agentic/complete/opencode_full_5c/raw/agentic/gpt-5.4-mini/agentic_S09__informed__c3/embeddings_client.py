import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    model: str


def load_config(model: Optional[str] = None) -> EmbeddingsConfig:
    return EmbeddingsConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        model=model
        or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    )


def create_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
