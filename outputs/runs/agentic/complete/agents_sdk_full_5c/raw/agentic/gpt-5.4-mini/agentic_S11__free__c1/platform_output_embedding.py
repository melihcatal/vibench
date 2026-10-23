from __future__ import annotations

from typing import List, Optional

from openai import OpenAI

from model_client import DEFAULT_EMBEDDING_MODEL, get_client


def platform_output_embedding(text: str, client: Optional[OpenAI] = None) -> List[float]:
    client = client or get_client()
    response = client.embeddings.create(model=DEFAULT_EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
