from __future__ import annotations

from speech_client import OPENAI_BASE_URL, build_json_headers, request_json
from speech_models import EmbeddingResult


def embed_script(text: str, model: str = "text-embedding-3-small") -> EmbeddingResult:
    response = request_json(
        "POST",
        f"{OPENAI_BASE_URL}/embeddings",
        headers=build_json_headers("openai"),
        json={"model": model, "input": text},
    )
    embedding = response["data"][0]["embedding"]
    return EmbeddingResult(
        embedding=embedding,
        dimensions=len(embedding),
        provider="openai",
        model=model,
    )
