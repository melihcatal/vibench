import openai
import os
from typing import List


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    """
    Generate embeddings for translated segments using OpenAI text-embedding-3-small for translation memory search.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=segments, model="text-embedding-3-small")
    return [datum.embedding for datum in response.data]
