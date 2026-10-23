import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

from openai import OpenAI


@dataclass(frozen=True)
class PlatformEmbeddingConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    model: str = "text-embedding-3-small"


@dataclass(frozen=True)
class PlatformEmbeddingResult:
    vector: List[float]
    model: str
    provider: str
    input: str
    usage: Optional[Dict[str, Any]] = None
    response_id: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def load_platform_embedding_config() -> PlatformEmbeddingConfig:
    return PlatformEmbeddingConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORG_ID") or os.getenv("OPENAI_ORGANIZATION"),
        project=os.getenv("OPENAI_PROJECT"),
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    )


def create_platform_embedding_client(config: Optional[PlatformEmbeddingConfig] = None) -> OpenAI:
    cfg = config or load_platform_embedding_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def _coerce_text(value: Union[str, Sequence[Any], Dict[str, Any]]) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if isinstance(value.get("text"), str):
            return value["text"]
        if isinstance(value.get("content"), str):
            return value["content"]
        return str(value)
    return "\n".join(str(item) for item in value)


def embed_platform_output(
    output: Union[str, Sequence[Any], Dict[str, Any]],
    *,
    model: Optional[str] = None,
    config: Optional[PlatformEmbeddingConfig] = None,
) -> PlatformEmbeddingResult:
    cfg = config or load_platform_embedding_config()
    client = create_platform_embedding_client(cfg)
    text = _coerce_text(output)
    embedding_model = model or cfg.model
    response = client.embeddings.create(model=embedding_model, input=text)
    first = response.data[0]
    usage = getattr(response, "usage", None)
    return PlatformEmbeddingResult(
        vector=list(first.embedding),
        model=getattr(response, "model", embedding_model),
        provider="openai",
        input=text,
        usage=usage.model_dump() if hasattr(usage, "model_dump") else usage,
        response_id=getattr(response, "id", None),
        raw=response.model_dump() if hasattr(response, "model_dump") else None,
    )
