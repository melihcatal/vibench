from __future__ import annotations

from openai import OpenAI

from storage_models import EmbeddingResult, StorageObjectRef


EMBED_MODEL = "text-embedding-3-small"


def asset_metadata_embedding(bucket: str, key: str, metadata: dict | None = None, extracted_text: str = "") -> EmbeddingResult:
    client = OpenAI()
    text = f"Metadata: {metadata or {}}\n\nExtracted text: {extracted_text}".strip()
    resp = client.embeddings.create(model=EMBED_MODEL, input=text)
    vector = list(resp.data[0].embedding)
    return EmbeddingResult(source=StorageObjectRef(bucket=bucket, key=key), vector=vector, dimensions=len(vector), provider="openai", raw=resp.model_dump())
