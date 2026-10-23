from typing import List

from openai import OpenAI


def moderation_reason_embedding(text: str) -> List[float]:
    client = OpenAI()
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    return result.data[0].embedding
