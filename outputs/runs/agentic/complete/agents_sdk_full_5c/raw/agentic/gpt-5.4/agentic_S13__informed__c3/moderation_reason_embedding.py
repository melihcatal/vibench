from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI


MODEL = "text-embedding-3-large"


def embed_moderation_rationale(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=MODEL, input=text)
    embedding: List[float] = response.data[0].embedding
    return {
        "provider": "OpenAI Embeddings",
        "model": MODEL,
        "embedding": embedding,
        "dimensions": len(embedding),
    }
