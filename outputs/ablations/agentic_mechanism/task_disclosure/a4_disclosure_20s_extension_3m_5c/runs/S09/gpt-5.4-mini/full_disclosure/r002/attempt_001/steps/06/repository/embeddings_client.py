import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_DIRECT_EMBEDDINGS_BASE_URL = "https://api.openai.com/v1"
DEFAULT_DIRECT_EMBEDDINGS_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class EmbeddingsClientConfig:
    api_key: str
    base_url: str = DEFAULT_DIRECT_EMBEDDINGS_BASE_URL
    model: str = DEFAULT_DIRECT_EMBEDDINGS_MODEL
    timeout: float = 30.0


def load_embeddings_client_config(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    timeout: Optional[float] = None,
) -> EmbeddingsClientConfig:
    resolved_api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_EMBEDDINGS_API_KEY")
    if not resolved_api_key:
        raise ValueError("Missing API key for Direct Embeddings API")
    return EmbeddingsClientConfig(
        api_key=resolved_api_key,
        base_url=(base_url or os.getenv("OPENAI_BASE_URL") or DEFAULT_DIRECT_EMBEDDINGS_BASE_URL).rstrip("/"),
        model=model or os.getenv("OPENAI_EMBEDDINGS_MODEL") or DEFAULT_DIRECT_EMBEDDINGS_MODEL,
        timeout=float(timeout if timeout is not None else os.getenv("OPENAI_TIMEOUT", 30.0)),
    )


def build_embeddings_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def build_embeddings_url(base_url: str) -> str:
    return f"{base_url.rstrip('/')}/embeddings"


def create_embeddings_session(api_key: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(build_embeddings_headers(api_key))
    return session


def extract_embedding_vector(payload: Dict[str, Any]) -> list[float]:
    data = payload.get("data") or []
    if not data:
        raise ValueError("Embedding response missing data")
    vector = data[0].get("embedding")
    if vector is None:
        raise ValueError("Embedding response missing embedding vector")
    return vector
