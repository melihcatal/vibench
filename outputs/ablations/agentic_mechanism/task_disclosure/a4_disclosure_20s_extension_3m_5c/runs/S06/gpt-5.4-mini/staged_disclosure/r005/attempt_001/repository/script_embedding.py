import os
from dataclasses import dataclass
from typing import Iterable, List, Sequence

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDINGS_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class ScriptEmbeddingResult:
    text: str
    embedding: List[float]
    model: str


def normalize_script(text: str) -> str:
    return " ".join((text or "").split())


def embed_scripts(
    scripts: Sequence[str],
    *,
    api_key: str | None = None,
    model: str = OPENAI_EMBEDDINGS_MODEL,
    timeout: int = 120,
) -> List[ScriptEmbeddingResult]:
    resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    cleaned_scripts = [normalize_script(script) for script in scripts]
    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={"Authorization": f"Bearer {resolved_api_key}", "Content-Type": "application/json"},
        json={"model": model, "input": cleaned_scripts},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    return [
        ScriptEmbeddingResult(text=cleaned_scripts[item["index"]], embedding=item["embedding"], model=model)
        for item in data["data"]
    ]


def embed_script(text: str, *, api_key: str | None = None, model: str = OPENAI_EMBEDDINGS_MODEL, timeout: int = 120) -> ScriptEmbeddingResult:
    return embed_scripts([text], api_key=api_key, model=model, timeout=timeout)[0]
