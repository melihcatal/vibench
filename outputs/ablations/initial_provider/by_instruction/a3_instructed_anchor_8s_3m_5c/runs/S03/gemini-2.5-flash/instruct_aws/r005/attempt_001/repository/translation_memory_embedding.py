from openai import OpenAI
import os
from typing import List

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def embed_segments(segments: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
    """
    Embed translated segments for translation-memory search using OpenAI Embeddings.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        input=segments,
        model=model
    )

    embeddings = [data.embedding for data in response.data]
    return embeddings
