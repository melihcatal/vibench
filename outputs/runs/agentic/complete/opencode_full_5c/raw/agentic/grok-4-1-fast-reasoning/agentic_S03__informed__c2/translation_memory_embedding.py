import os
from openai import OpenAI
from typing import List


def embed_translated_segments(texts: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embeddings = []
    for text in texts:
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        embeddings.append(response.data[0].embedding)
    return embeddings


def embed_single_translation_memory_segment(text: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding
