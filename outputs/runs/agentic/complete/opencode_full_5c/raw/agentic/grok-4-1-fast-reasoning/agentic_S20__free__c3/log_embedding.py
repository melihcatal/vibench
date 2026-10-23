import openai
import os
from typing import List


def generate_log_embeddings(messages: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = openai.OpenAI(api_key=api_key)
    response = client.embeddings.create(model="text-embedding-3-small", input=messages)
    return [embedding.embedding for embedding in response.data]
