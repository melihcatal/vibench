import os
from dataclasses import dataclass
from typing import Iterable, List, Sequence

import requests


DEFAULT_API_BASE = "https://api.openai.com/v1"
DEFAULT_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    api_base: str = DEFAULT_API_BASE
    model: str = DEFAULT_MODEL
    timeout: float = 60.0


def load_config() -> EmbeddingsConfig:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    api_base = os.getenv("OPENAI_API_BASE", DEFAULT_API_BASE).strip() or DEFAULT_API_BASE
    model = os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    timeout = float(os.getenv("OPENAI_TIMEOUT", "60"))
    return EmbeddingsConfig(api_key=api_key, api_base=api_base.rstrip("/"), model=model, timeout=timeout)


class DirectEmbeddingsClient:
    def __init__(self, config: EmbeddingsConfig | None = None):
        self.config = config or load_config()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def embed(self, input_text: str) -> List[float]:
        return self.embed_many([input_text])[0]

    def embed_many(self, inputs: Sequence[str]) -> List[List[float]]:
        if not inputs:
            return []
        response = self._session.post(
            f"{self.config.api_base}/embeddings",
            json={"model": self.config.model, "input": list(inputs)},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        data = payload.get("data", [])
        return [item["embedding"] for item in sorted(data, key=lambda x: x.get("index", 0))]


def get_client() -> DirectEmbeddingsClient:
    return DirectEmbeddingsClient()


def embed_text(text: str) -> List[float]:
    return get_client().embed(text)


def embed_texts(texts: Iterable[str]) -> List[List[float]]:
    return get_client().embed_many(list(texts))
