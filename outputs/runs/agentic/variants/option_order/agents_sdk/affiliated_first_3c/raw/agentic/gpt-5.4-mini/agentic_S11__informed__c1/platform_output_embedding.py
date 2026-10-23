from __future__ import annotations

import os

from openai import OpenAI

from model_models import EmbeddingResult


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_output(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    vector = response.data[0].embedding
    return EmbeddingResult(vector=vector, model=EMBEDDING_MODEL, raw=response)
