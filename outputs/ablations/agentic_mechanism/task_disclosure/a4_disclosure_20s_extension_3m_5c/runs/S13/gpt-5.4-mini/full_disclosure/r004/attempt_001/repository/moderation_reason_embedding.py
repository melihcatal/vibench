import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests


OPENAI_EMBEDDING_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@dataclass(frozen=True)
class ModerationReasonEmbeddingConfig:
    api_key: Optional[str] = None
    model: str = OPENAI_EMBEDDING_MODEL
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "ModerationReasonEmbeddingConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL),
            timeout=float(os.getenv("OPENAI_EMBEDDING_TIMEOUT", "30")),
        )


def _resolve_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def _coerce_texts(texts: Any) -> List[str]:
    if isinstance(texts, str):
        return [texts]
    if isinstance(texts, Sequence) and not isinstance(texts, (bytes, bytearray)):
        normalized = list(texts)
        if all(isinstance(item, str) for item in normalized):
            return normalized
    raise TypeError("text must be a string or sequence of strings")


def _build_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    return {"Authorization": f"Bearer {_resolve_api_key(api_key)}", "Content-Type": "application/json"}


def embed_moderation_reasons(
    reasons: Any,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    timeout: Optional[float] = None,
) -> Dict[str, Any]:
    input_texts = _coerce_texts(reasons)
    payload = {"model": model or OPENAI_EMBEDDING_MODEL, "input": input_texts}
    response = requests.post(
        OPENAI_EMBEDDING_API_URL,
        headers=_build_headers(api_key),
        json=payload,
        timeout=timeout if timeout is not None else 30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "provider": "openai",
        "model": data.get("model", payload["model"]),
        "embeddings": [item.get("embedding", []) for item in data.get("data", [])],
        "raw": data,
    }


def embed_single_moderation_reason(
    reason: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    timeout: Optional[float] = None,
) -> Dict[str, Any]:
    result = embed_moderation_reasons(reason, api_key=api_key, model=model, timeout=timeout)
    embedding = result["embeddings"][0] if result["embeddings"] else []
    return {"provider": result["provider"], "model": result["model"], "embedding": embedding, "raw": result["raw"]}
