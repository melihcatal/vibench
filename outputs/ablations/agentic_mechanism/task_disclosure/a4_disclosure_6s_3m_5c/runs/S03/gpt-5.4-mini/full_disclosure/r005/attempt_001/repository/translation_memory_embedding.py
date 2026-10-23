import os
from typing import List, Sequence

from openai import OpenAI


def embed_translated_segments(segments: Sequence[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=list(segments))
    return [item.embedding for item in response.data]
