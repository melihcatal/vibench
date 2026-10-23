from __future__ import annotations

import json
import os
from typing import Any, Mapping, Optional

from openai import OpenAI

from storage_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def embed_asset_metadata(
    bucket: str,
    key: str,
    metadata: Mapping[str, Any],
    extracted_text: Optional[str] = None,
) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    payload = {
        "bucket": bucket,
        "key": key,
        "metadata": dict(metadata),
        "extracted_text": extracted_text or "",
    }
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=json.dumps(payload, sort_keys=True, ensure_ascii=False),
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        embedding=vector,
        dimensions=len(vector),
        model=OPENAI_EMBEDDING_MODEL,
    )
