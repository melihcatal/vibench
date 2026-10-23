from __future__ import annotations

import json

from openai import OpenAI

from storage_models import EmbeddingResult


def embed_asset_metadata(
    metadata: dict[str, object], extracted_text: str
) -> EmbeddingResult:
    client = OpenAI()
    content = (
        json.dumps(metadata, sort_keys=True, ensure_ascii=False) + "\n" + extracted_text
    )
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=content,
    )
    vector = list(response.data[0].embedding)
    return EmbeddingResult(
        vector=vector,
        dimensions=len(vector),
        provider="openai",
        model="text-embedding-3-large",
    )
