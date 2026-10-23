import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
DEFAULT_TIMEOUT = float(os.getenv("OPENAI_EMBEDDINGS_TIMEOUT", "60"))


@dataclass(frozen=True)
class EmbeddingsClientConfig:
    api_key: str
    model: str = DEFAULT_EMBEDDING_MODEL
    api_base: str = DEFAULT_API_BASE
    timeout: float = DEFAULT_TIMEOUT


def get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def get_default_config(model: Optional[str] = None) -> EmbeddingsClientConfig:
    return EmbeddingsClientConfig(api_key=get_api_key(), model=model or DEFAULT_EMBEDDING_MODEL)


def create_session(api_key: Optional[str] = None) -> requests.Session:
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {api_key or get_api_key()}", "Content-Type": "application/json"})
    return session


def embeddings_endpoint(api_base: Optional[str] = None) -> str:
    return f"{api_base or DEFAULT_API_BASE}/embeddings"


def post_embeddings(texts: List[str], config: Optional[EmbeddingsClientConfig] = None) -> Dict[str, Any]:
    if not isinstance(texts, list):
        raise TypeError("texts must be a list of strings")
    if not texts:
        raise ValueError("texts must not be empty")

    cfg = config or get_default_config()
    session = create_session(cfg.api_key)
    response = session.post(
        embeddings_endpoint(cfg.api_base),
        json={"model": cfg.model, "input": texts},
        timeout=cfg.timeout,
    )
    response.raise_for_status()
    return response.json()


def extract_embeddings(payload: Dict[str, Any]) -> List[List[float]]:
    data = sorted(payload["data"], key=lambda item: item["index"])
    return [item["embedding"] for item in data]
