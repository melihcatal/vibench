import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


DEFAULT_EMBEDDINGS_MODEL = os.getenv("DIRECT_EMBEDDINGS_MODEL", "text-embedding-3-small")
DEFAULT_API_BASE = os.getenv("DIRECT_EMBEDDINGS_API_BASE", "https://api.openai.com/v1")
DEFAULT_TIMEOUT = float(os.getenv("DIRECT_EMBEDDINGS_TIMEOUT", "30"))


@dataclass(frozen=True)
class EmbeddingsConfig:
    api_key: str
    model: str = DEFAULT_EMBEDDINGS_MODEL
    api_base: str = DEFAULT_API_BASE
    timeout: float = DEFAULT_TIMEOUT

    @classmethod
    def from_env(cls) -> "EmbeddingsConfig":
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("DIRECT_EMBEDDINGS_API_KEY")
        if not api_key:
            raise ValueError("Missing API key: set OPENAI_API_KEY or DIRECT_EMBEDDINGS_API_KEY")
        return cls(api_key=api_key)


class DirectEmbeddingsClient:
    def __init__(self, config: Optional[EmbeddingsConfig] = None) -> None:
        self.config = config or EmbeddingsConfig.from_env()

    def embed(self, input_texts: List[str]) -> List[List[float]]:
        if not input_texts:
            raise ValueError("input_texts must not be empty")

        response = requests.post(
            f"{self.config.api_base.rstrip('/')}/embeddings",
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": self.config.model, "input": input_texts},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        payload: Dict[str, Any] = response.json()
        data = payload.get("data", [])
        return [item["embedding"] for item in data]

    def embed_one(self, input_text: str) -> List[float]:
        return self.embed([input_text])[0]
