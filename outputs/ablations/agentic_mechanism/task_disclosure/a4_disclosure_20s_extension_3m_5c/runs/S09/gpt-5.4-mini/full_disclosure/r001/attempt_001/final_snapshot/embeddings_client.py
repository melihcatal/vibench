import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class EmbeddingsClientConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    timeout: float = 30.0


def get_config() -> EmbeddingsClientConfig:
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("EMBEDDINGS_API_KEY")
    if not api_key:
        raise ValueError("Missing API key; set OPENAI_API_KEY or EMBEDDINGS_API_KEY")
    return EmbeddingsClientConfig(
        api_key=api_key,
        base_url=os.environ.get("OPENAI_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
        model=os.environ.get("OPENAI_EMBEDDING_MODEL", DEFAULT_MODEL),
        timeout=float(os.environ.get("EMBEDDINGS_TIMEOUT", "30")),
    )


def create_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    token = api_key or get_config().api_key
    session.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    return session


def build_embeddings_request(texts: Any, model: Optional[str] = None, dimensions: Optional[int] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"input": texts, "model": model or get_config().model}
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def embeddings_url(base_url: Optional[str] = None) -> str:
    return f"{(base_url or get_config().base_url).rstrip('/')}/embeddings"


def post_embeddings(texts: Any, *, model: Optional[str] = None, dimensions: Optional[int] = None, timeout: Optional[float] = None, base_url: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    config = get_config()
    session = create_session(api_key=api_key or config.api_key)
    response = session.post(
        embeddings_url(base_url or config.base_url),
        json=build_embeddings_request(texts, model=model or config.model, dimensions=dimensions),
        timeout=timeout or config.timeout,
    )
    response.raise_for_status()
    return response.json()
