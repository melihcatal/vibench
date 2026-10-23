import os
from typing import Iterable, List, Sequence

from openai import OpenAI


def embed_translated_segments(segments: Sequence[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=list(segments))
    return [item.embedding for item in response.data]


def embed_translated_segment(segment: str, model: str = "text-embedding-3-small") -> List[float]:
    return embed_translated_segments([segment], model=model)[0]


def batch_embed_translated_segments(segments: Iterable[str], batch_size: int = 100, model: str = "text-embedding-3-small") -> List[List[float]]:
    all_embeddings: List[List[float]] = []
    batch: List[str] = []
    for segment in segments:
        batch.append(segment)
        if len(batch) >= batch_size:
            all_embeddings.extend(embed_translated_segments(batch, model=model))
            batch = []
    if batch:
        all_embeddings.extend(embed_translated_segments(batch, model=model))
    return all_embeddings
