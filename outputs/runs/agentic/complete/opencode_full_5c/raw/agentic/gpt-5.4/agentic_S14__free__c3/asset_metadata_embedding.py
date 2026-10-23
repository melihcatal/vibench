from __future__ import annotations

from storage_client import get_openai_client
from storage_models import EmbeddingResult


def embed_asset_metadata(
    metadata: dict[str, str] | None, extracted_text: str
) -> EmbeddingResult:
    client = get_openai_client()
    metadata_lines = "\n".join(f"{k}: {v}" for k, v in sorted((metadata or {}).items()))
    content = f"Metadata:\n{metadata_lines}\n\nExtracted text:\n{extracted_text}"
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=content,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(vector=vector, model="text-embedding-3-large")
