from __future__ import annotations

import json
import os

from openai import OpenAI

from storage_models import AssetEmbeddingResult


def embed_asset_metadata(
    metadata: dict[str, str] | None, extracted_text: str
) -> AssetEmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    serialized = json.dumps(metadata or {}, sort_keys=True)
    input_text = f"metadata={serialized}\ncontent={extracted_text}"
    response = client.embeddings.create(
        model="text-embedding-3-large", input=input_text
    )
    embedding = response.data[0].embedding
    return AssetEmbeddingResult(
        embedding=embedding,
        model="text-embedding-3-large",
        provider="openai",
        dimensions=len(embedding),
    )
