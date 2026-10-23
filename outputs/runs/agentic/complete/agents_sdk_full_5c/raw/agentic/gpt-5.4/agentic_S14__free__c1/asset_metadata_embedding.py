from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI

from storage_models import EmbeddingResult


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def embed_asset_metadata(metadata: Dict[str, Any], extracted_text: str = "", model: Optional[str] = None) -> EmbeddingResult:
    resolved_model = model or DEFAULT_EMBEDDING_MODEL
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    payload = {
        "metadata": metadata,
        "extracted_text": extracted_text,
    }
    embedding = client.embeddings.create(
        model=resolved_model,
        input=json.dumps(payload, sort_keys=True, ensure_ascii=False),
    ).data[0].embedding

    return EmbeddingResult(
        provider="openai",
        model=resolved_model,
        dimensions=len(embedding),
        vector=embedding,
    )
