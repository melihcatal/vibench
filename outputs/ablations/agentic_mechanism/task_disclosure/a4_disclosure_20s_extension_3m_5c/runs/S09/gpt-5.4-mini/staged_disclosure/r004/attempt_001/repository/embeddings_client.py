import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_EMBEDDINGS_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def load_embeddings_config() -> Dict[str, Any]:
    return {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": os.getenv("OPENAI_BASE_URL", OPENAI_EMBEDDINGS_API_URL),
        "model": os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_DEFAULT_EMBEDDING_MODEL),
        "timeout": float(os.getenv("OPENAI_EMBEDDINGS_TIMEOUT", "30")),
    }


def create_embeddings_client(api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: Optional[float] = None) -> "EmbeddingsClient":
    config = load_embeddings_config()
    return EmbeddingsClient(
        api_key=api_key or config["api_key"],
        base_url=base_url or config["base_url"],
        timeout=timeout if timeout is not None else config["timeout"],
        model=config["model"],
    )


class EmbeddingsClient:
    def __init__(self, api_key: str, base_url: str, timeout: float, model: str) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.model = model

    def embed(self, input_texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        payload = {"input": input_texts, "model": model or self.model}
        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]


def embed_text(text: str, model: Optional[str] = None) -> List[float]:
    return create_embeddings_client().embed([text], model=model)[0]
