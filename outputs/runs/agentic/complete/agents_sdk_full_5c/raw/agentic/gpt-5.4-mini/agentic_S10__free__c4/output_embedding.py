from __future__ import annotations

import os

from openai import OpenAI

from model_client import build_openai_client, resolve_embedding_model
from model_models import extract_embedding_vector


def embed_output(text: str, *, client: OpenAI | None = None, model: str | None = None) -> list[float]:
    api_client = client or build_openai_client()
    model_name = model or resolve_embedding_model()
    response = api_client.embeddings.create(model=model_name, input=text)
    return extract_embedding_vector(response)


if __name__ == "__main__":
    sample = os.environ.get("EMBED_TEXT", "")
    if sample:
        print(embed_output(sample))
