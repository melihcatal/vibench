import os
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_BASE_URL = os.getenv("OPENAI_BASE_URL")


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    model: str = DEFAULT_EMBEDDING_MODEL
    base_url: str | None = DEFAULT_BASE_URL


def load_config() -> EmbeddingsConfig:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return EmbeddingsConfig(
        api_key=api_key,
        model=os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        base_url=os.getenv("OPENAI_BASE_URL", DEFAULT_BASE_URL) or None,
    )


def create_client(config: EmbeddingsConfig | None = None) -> OpenAI:
    config = config or load_config()
    kwargs = {"api_key": config.api_key}
    if config.base_url:
        kwargs["base_url"] = config.base_url
    return OpenAI(**kwargs)


def embed_text(text: str, config: EmbeddingsConfig | None = None) -> List[float]:
    config = config or load_config()
    client = create_client(config)
    response = client.embeddings.create(model=config.model, input=text)
    return list(response.data[0].embedding)


def embed_texts(texts: Sequence[str], config: EmbeddingsConfig | None = None) -> List[List[float]]:
    config = config or load_config()
    client = create_client(config)
    response = client.embeddings.create(model=config.model, input=list(texts))
    return [list(item.embedding) for item in response.data]


def normalize_vector(vector: Iterable[float]) -> List[float]:
    values = list(vector)
    magnitude = sum(v * v for v in values) ** 0.5
    if magnitude == 0:
        return values
    return [v / magnitude for v in values]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vectors must have the same length")
    return sum(a * b for a, b in zip(left, right))
