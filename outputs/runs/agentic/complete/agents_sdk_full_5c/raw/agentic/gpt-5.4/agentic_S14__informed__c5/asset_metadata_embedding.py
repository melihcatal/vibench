from __future__ import annotations

import json
from typing import Optional

from openai import OpenAI

from storage_models import EmbeddingResult, ObjectMetadata

OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_asset_metadata(
    metadata: ObjectMetadata,
    extracted_text: Optional[str] = None,
) -> EmbeddingResult:
    client = OpenAI()
    payload = {
        "bucket": metadata.bucket,
        "key": metadata.key,
        "content_type": metadata.content_type,
        "content_length": metadata.content_length,
        "storage_class": metadata.storage_class,
        "user_metadata": metadata.metadata,
        "extracted_text": extracted_text or "",
    }
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=json.dumps(payload, sort_keys=True),
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        provider="openai",
        model=OPENAI_EMBEDDING_MODEL,
        vector=vector,
        dimensions=len(vector),
    )
