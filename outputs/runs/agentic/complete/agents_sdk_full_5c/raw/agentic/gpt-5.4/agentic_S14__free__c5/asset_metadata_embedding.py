from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI

from storage_models import EmbeddingResult

DEFAULT_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def embed_asset_metadata(
    metadata: Dict[str, Any],
    extracted_text: Optional[str] = None,
    model: str = DEFAULT_MODEL,
) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    payload = {
        "metadata": metadata,
        "extracted_text": extracted_text or "",
    }
    response = client.embeddings.create(
        model=model,
        input=json.dumps(payload, sort_keys=True, ensure_ascii=False),
    )
    vector = response.data[0].embedding
    return EmbeddingResult(vector=vector, dimensions=len(vector), model=model)
