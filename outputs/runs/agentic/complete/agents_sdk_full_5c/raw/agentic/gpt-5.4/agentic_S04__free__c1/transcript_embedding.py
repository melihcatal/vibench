from __future__ import annotations

import os
from typing import Dict, Iterable, Optional

from openai import OpenAI

from speech_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(segments: Iterable[str], *, api_key: Optional[str] = None) -> Dict[str, object]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    texts = [segment for segment in segments if segment]
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    vectors = [item.embedding for item in response.data]
    result = EmbeddingResult(vectors=vectors, model=OPENAI_EMBEDDING_MODEL)
    return {
        "provider": "openai",
        "model": result.model,
        "count": len(result.vectors),
        "embeddings": result.vectors,
    }
