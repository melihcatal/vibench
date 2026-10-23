from __future__ import annotations

import os

from openai import OpenAI

from observability_models import EmbeddingResult

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_log_message(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    vector = list(response.data[0].embedding)
    return EmbeddingResult(vector=vector, model=OPENAI_EMBEDDING_MODEL, raw_response=response)
