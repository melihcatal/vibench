import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_EMBEDDINGS_API_HOST = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDINGS_MODEL = os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")


@dataclass(frozen=True)
class EmbeddingsClientConfig:
    api_key: str
    model: str = OPENAI_EMBEDDINGS_MODEL
    base_url: str = OPENAI_EMBEDDINGS_API_HOST
    timeout: float = 60.0


def get_embeddings_client_config(api_key: Optional[str] = None, model: Optional[str] = None) -> EmbeddingsClientConfig:
    resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved_api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return EmbeddingsClientConfig(api_key=resolved_api_key, model=model or OPENAI_EMBEDDINGS_MODEL)


def build_embeddings_headers(api_key: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def create_embeddings_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


def post_embeddings_request(text_input: Any, config: Optional[EmbeddingsClientConfig] = None) -> Dict[str, Any]:
    resolved_config = config or get_embeddings_client_config()
    response = requests.post(
        resolved_config.base_url,
        headers=build_embeddings_headers(resolved_config.api_key),
        json={"model": resolved_config.model, "input": text_input},
        timeout=resolved_config.timeout,
    )
    response.raise_for_status()
    return response.json()
