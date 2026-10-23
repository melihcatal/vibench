import os
from typing import List
import openai


def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    """
    Embed transcript segments for semantic retrieval using OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(input=segments, model="text-embedding-3-small")

    return [embedding.embedding for embedding in response.data]
