import os
from typing import List
from openai import OpenAI


def embed_moderation_rationale(rationale: str) -> List[float]:
    if not rationale.strip():
        return []
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=rationale)
    return response.data[0].embedding


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small", input=rationales
    )
    return [data.embedding for data in response.data]
