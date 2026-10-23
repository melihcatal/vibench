import os
from typing import List

from openai import OpenAI


def embed_messages(messages: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-large", input=messages)
    return [item.embedding for item in response.data]
