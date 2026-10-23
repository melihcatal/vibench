import os
from typing import List
import openai


def moderation_reason_embedding(reasons: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OpenAI API key not configured")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model="text-embedding-3-small", input=reasons, encoding_format="float"
    )

    embeddings = [data.embedding for data in response.data]
    return embeddings
