import os
from dataclasses import dataclass
from typing import List, Optional, Sequence

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL
    base_url: str = OPENAI_EMBEDDINGS_URL
    timeout: float = 30.0


def load_config(api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None, timeout: Optional[float] = None) -> EmbeddingsConfig:
    resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return EmbeddingsConfig(
        api_key=resolved_api_key,
        model=model or os.environ.get("OPENAI_EMBEDDING_MODEL", DEFAULT_OPENAI_EMBEDDING_MODEL),
        base_url=base_url or os.environ.get("OPENAI_EMBEDDINGS_URL", OPENAI_EMBEDDINGS_URL),
        timeout=float(timeout if timeout is not None else os.environ.get("OPENAI_EMBEDDINGS_TIMEOUT", 30.0)),
    )


class DirectEmbeddingsClient:
    def __init__(self, config: EmbeddingsConfig):
        self.config = config

    def embed(self, inputs: Sequence[str]) -> List[List[float]]:
        response = requests.post(
            self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": self.config.model, "input": list(inputs)},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        return [item["embedding"] for item in sorted(payload["data"], key=lambda x: x["index"])]


def create_client(api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None, timeout: Optional[float] = None) -> DirectEmbeddingsClient:
    return DirectEmbeddingsClient(load_config(api_key=api_key, model=model, base_url=base_url, timeout=timeout))


def embed_text(text: str, api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None, timeout: Optional[float] = None) -> List[float]:
    return create_client(api_key=api_key, model=model, base_url=base_url, timeout=timeout).embed([text])[0]


def embed_texts(texts: Sequence[str], api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None, timeout: Optional[float] = None) -> List[List[float]]:
    return create_client(api_key=api_key, model=model, base_url=base_url, timeout=timeout).embed(texts)
