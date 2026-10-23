import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests


@dataclass
class EmbeddingRequest:
    messages: Sequence[str]
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResult:
    embeddings: List[List[float]]
    model: str
    usage: Optional[Dict[str, Any]] = None


def _load_openai_config(env: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    source = env if env is not None else os.environ
    return {
        "api_key": source.get("OPENAI_API_KEY", ""),
        "api_base_url": source.get("OPENAI_BASE_URL", "https://api.openai.com"),
    }


def embed_log_messages(messages: Iterable[str], model: str = "text-embedding-3-small", env: Optional[Dict[str, str]] = None) -> EmbeddingResult:
    config = _load_openai_config(env)
    payload = {
        "input": list(messages),
        "model": model,
    }
    response = requests.post(
        f"{config['api_base_url'].rstrip('/')}/v1/embeddings",
        headers={
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    embeddings = [item["embedding"] for item in data.get("data", [])]
    return EmbeddingResult(embeddings=embeddings, model=data.get("model", model), usage=data.get("usage"))
