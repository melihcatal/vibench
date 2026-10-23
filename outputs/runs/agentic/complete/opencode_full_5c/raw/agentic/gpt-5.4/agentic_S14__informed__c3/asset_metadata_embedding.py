from __future__ import annotations

from openai import OpenAI

from storage_client import require_openai_api_key
from storage_models import EmbeddingResult


def embed_asset_metadata(
    metadata: dict[str, str] | None, extracted_text: str
) -> EmbeddingResult:
    client = OpenAI(api_key=require_openai_api_key())
    metadata_text = "\n".join(f"{k}: {v}" for k, v in (metadata or {}).items())
    payload = f"Metadata:\n{metadata_text}\n\nExtracted Text:\n{extracted_text}"
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=payload,
    )
    item = response.data[0]
    return EmbeddingResult(
        vector=item.embedding,
        model="text-embedding-3-large",
        dimensions=len(item.embedding),
    )
