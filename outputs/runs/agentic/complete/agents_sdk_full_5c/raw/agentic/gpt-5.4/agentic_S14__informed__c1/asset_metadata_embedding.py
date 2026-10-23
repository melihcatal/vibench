from __future__ import annotations

import json
import os
from typing import Any, Mapping, Optional

from openai import OpenAI

from storage_models import EmbeddingResult


_DEFAULT_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")


def embed_asset_metadata(
    bucket: str,
    key: str,
    metadata: Optional[Mapping[str, Any]] = None,
    extracted_text: str = "",
) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    payload = {
        "bucket": bucket,
        "key": key,
        "metadata": dict(metadata or {}),
        "extracted_text": extracted_text,
    }
    response = client.embeddings.create(
        model=_DEFAULT_EMBED_MODEL,
        input=json.dumps(payload, ensure_ascii=False),
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        provider="OpenAI",
        model=_DEFAULT_EMBED_MODEL,
        vector=vector,
        dimensions=len(vector),
        raw=response.model_dump(),
    )
