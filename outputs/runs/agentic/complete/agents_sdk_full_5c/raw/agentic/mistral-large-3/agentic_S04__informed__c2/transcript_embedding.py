import os
from typing import List
from openai import OpenAI

def transcript_embedding(text_segments: List[str]) -> List[List[float]]:
    """
    Generate embeddings for transcript segments using OpenAI's text-embedding-ada-002 model.
    Returns a list of embedding vectors for each segment.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embeddings = []
    for segment in text_segments:
        response = client.embeddings.create(
            input=segment,
            model="text-embedding-ada-002"
        )
        embeddings.append(response.data[0].embedding)
    return embeddings