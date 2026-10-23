import os
from typing import Iterable, List, Sequence

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_translated_segments(segments: Sequence[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    client = _client()
    response = client.embeddings.create(model=model, input=list(segments))
    return [item.embedding for item in response.data]


def embed_translated_segment(segment: str, model: str = "text-embedding-3-small") -> List[float]:
    return embed_translated_segments([segment], model=model)[0]
