from __future__ import annotations

from storage_client import get_openai_client
from storage_models import EmbeddingResult, ObjectMetadata


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_asset_metadata(metadata: ObjectMetadata, extracted_text: str | None = None) -> EmbeddingResult:
    client = get_openai_client()
    input_text = "\n".join(
        [
            f"bucket: {metadata.bucket}",
            f"key: {metadata.key}",
            f"content_type: {metadata.content_type or ''}",
            f"size: {metadata.size or ''}",
            f"etag: {metadata.etag or ''}",
            f"metadata: {metadata.metadata}",
            f"extracted_text: {extracted_text or ''}",
        ]
    )
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=input_text)
    vector = list(response.data[0].embedding)
    return EmbeddingResult(vector=vector, model=OPENAI_EMBEDDING_MODEL, dimensions=len(vector))
