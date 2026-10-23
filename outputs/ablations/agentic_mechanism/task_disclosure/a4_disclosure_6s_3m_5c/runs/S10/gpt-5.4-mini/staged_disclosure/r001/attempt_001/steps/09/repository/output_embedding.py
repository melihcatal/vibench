import os
from typing import Iterable, List, Sequence

import requests


OPENAI_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBED_MODEL = "text-embedding-3-small"


def _normalize_text(value: str) -> str:
    return " ".join(value.split())


def embed_outputs(outputs: Sequence[str], api_key: str | None = None, model: str = OPENAI_EMBED_MODEL) -> List[List[float]]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    payload = {"input": [_normalize_text(text) for text in outputs], "model": model}
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]


def embed_output_for_retrieval(output: str, api_key: str | None = None) -> List[float]:
    return embed_outputs([output], api_key=api_key)[0]


def embed_outputs_for_clustering(outputs: Iterable[str], api_key: str | None = None) -> List[List[float]]:
    return embed_outputs(list(outputs), api_key=api_key)
