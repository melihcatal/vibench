from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from observability_models import EmbeddingResult

MODEL_NAME = "text-embedding-3-small"



def log_embedding(messages: Iterable[str]) -> List[EmbeddingResult]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    inputs = list(messages)
    response = client.embeddings.create(
        model=MODEL_NAME,
        input=inputs,
    )
    return [
        EmbeddingResult(
            vector=item.embedding,
            dimensions=len(item.embedding),
            provider_model=MODEL_NAME,
        )
        for item in response.data
    ]
