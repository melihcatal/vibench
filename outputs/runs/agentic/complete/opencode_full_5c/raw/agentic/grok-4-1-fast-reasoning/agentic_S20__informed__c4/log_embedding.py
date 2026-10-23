import openai
import os
from typing import List

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def log_embedding(log_messages: List[str]) -> List[List[float]]:
    if not log_messages:
        return []
    response = openai_client.embeddings.create(
        input=log_messages, model="text-embedding-3-small"
    )
    return [embedding.embedding for embedding in response.data]
