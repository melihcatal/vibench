from __future__ import annotations

import os

from openai import OpenAI

from model_models import NormalizedEmbedding


def embed_output(text: str) -> NormalizedEmbedding:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    vector = resp.data[0].embedding
    return NormalizedEmbedding(vector=vector, model=resp.model, raw=resp)
