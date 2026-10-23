from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    vector = response.data[0].embedding
    return EmbeddingResult(
        embedding=vector, dimensions=len(vector), model=EMBEDDING_MODEL
    )
