from __future__ import annotations

import os

from openai import OpenAI

from storage_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def embed_asset_metadata(metadata: dict[str, str] | None, extracted_text: str | None = None) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    metadata_lines = [f"{k}: {v}" for k, v in (metadata or {}).items()]
    payload = "\n".join(metadata_lines)
    if extracted_text:
        payload = f"{payload}\n\nExtracted text:\n{extracted_text}".strip()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=payload)
    vector = response.data[0].embedding
    return EmbeddingResult(vector=vector, model=OPENAI_EMBEDDING_MODEL, dimensions=len(vector))


def embed_asset_metadata_dict(metadata: dict[str, str] | None, extracted_text: str | None = None) -> dict:
    return embed_asset_metadata(metadata=metadata, extracted_text=extracted_text).to_dict()
