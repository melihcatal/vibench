import os
from dataclasses import dataclass
from typing import Iterable, List, Optional

from openai import OpenAI


@dataclass(frozen=True)
class EmbeddingConfig:
    api_key: Optional[str] = None
    model: str = "text-embedding-3-small"
    batch_size: int = 32


def load_embedding_config() -> EmbeddingConfig:
    batch_size = os.getenv("OPENAI_EMBEDDING_BATCH_SIZE", "32")
    try:
        parsed_batch_size = max(1, int(batch_size))
    except ValueError:
        parsed_batch_size = 32
    return EmbeddingConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        batch_size=parsed_batch_size,
    )


def create_embedding_client(config: Optional[EmbeddingConfig] = None) -> OpenAI:
    cfg = config or load_embedding_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    return OpenAI(**kwargs)


def _normalize_script(text: str) -> str:
    return " ".join((text or "").split()).strip()


def embed_script(text: str, config: Optional[EmbeddingConfig] = None) -> List[float]:
    cfg = config or load_embedding_config()
    client = create_embedding_client(cfg)
    response = client.embeddings.create(model=cfg.model, input=_normalize_script(text))
    return list(response.data[0].embedding)


def embed_scripts(scripts: Iterable[str], config: Optional[EmbeddingConfig] = None) -> List[List[float]]:
    cfg = config or load_embedding_config()
    client = create_embedding_client(cfg)
    normalized_scripts = [_normalize_script(script) for script in scripts]
    embeddings: List[List[float]] = []
    for index in range(0, len(normalized_scripts), cfg.batch_size):
        batch = normalized_scripts[index:index + cfg.batch_size]
        response = client.embeddings.create(model=cfg.model, input=batch)
        embeddings.extend([list(item.embedding) for item in response.data])
    return embeddings
