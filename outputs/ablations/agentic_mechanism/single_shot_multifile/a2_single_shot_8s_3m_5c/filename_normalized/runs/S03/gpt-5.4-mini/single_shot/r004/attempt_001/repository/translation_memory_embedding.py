import os
from typing import List

from openai import OpenAI


def embed_translation_segments(segments: List[str], model: str = "text-embedding-3-large") -> List[List[float]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=model, input=segments)
    return [list(item.embedding) for item in response.data]
