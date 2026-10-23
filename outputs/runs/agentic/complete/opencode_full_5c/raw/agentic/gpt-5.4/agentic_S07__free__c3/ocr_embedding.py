from __future__ import annotations

from typing import Iterable, List

from document_client import OPENAI_EMBEDDINGS_URL, build_openai_headers, post_json
from document_models import EmbeddingResult


def embed_document_sections(sections: Iterable[str]) -> EmbeddingResult:
    inputs = list(sections)
    payload = {
        "model": "text-embedding-3-large",
        "input": inputs,
    }
    response_json = post_json(
        OPENAI_EMBEDDINGS_URL, payload, headers=build_openai_headers()
    )
    vectors: List[List[float]] = [
        item.get("embedding", []) for item in response_json.get("data", [])
    ]
    return EmbeddingResult(
        provider="openai",
        model="text-embedding-3-large",
        embeddings=vectors,
        raw_response=response_json,
    )
