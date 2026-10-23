import os
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@dataclass(frozen=True)
class EmbeddingConfig:
    api_key: str | None = None
    base_url: str | None = None
    organization: str | None = None
    project: str | None = None
    model: str = DEFAULT_EMBEDDING_MODEL


def load_embedding_config() -> EmbeddingConfig:
    return EmbeddingConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
        model=os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
    )


def create_openai_client(config: EmbeddingConfig | None = None) -> OpenAI:
    cfg = config or load_embedding_config()
    return OpenAI(
        api_key=cfg.api_key,
        base_url=cfg.base_url,
        organization=cfg.organization,
        project=cfg.project,
    )


def _normalize_inputs(outputs: str | Sequence[str] | Iterable[str]) -> List[str]:
    if isinstance(outputs, str):
        return [outputs]
    return [str(item) for item in outputs]


def embed_outputs(outputs: str | Sequence[str] | Iterable[str], model: str | None = None, config: EmbeddingConfig | None = None) -> List[List[float]]:
    cfg = config or load_embedding_config()
    client = create_openai_client(cfg)
    input_texts = _normalize_inputs(outputs)
    selected_model = model or cfg.model
    response = client.embeddings.create(model=selected_model, input=input_texts)
    return [item.embedding for item in response.data]


def embed_output(outputs: str | Sequence[str] | Iterable[str], model: str | None = None, config: EmbeddingConfig | None = None) -> List[float] | List[List[float]]:
    embeddings = embed_outputs(outputs, model=model, config=config)
    if isinstance(outputs, str):
        return embeddings[0]
    return embeddings
