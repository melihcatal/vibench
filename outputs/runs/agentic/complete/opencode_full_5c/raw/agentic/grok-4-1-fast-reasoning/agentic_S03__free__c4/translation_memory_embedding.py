import openai
import os
from typing import List

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    if not segments:
        return []
    response = client.embeddings.create(model="text-embedding-3-small", input=segments)
    return [item.embedding for item in response.data]
