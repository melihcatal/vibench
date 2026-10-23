import openai
import os
from typing import List

def log_embedding(log_messages: List[str]) -> List[List[float]]:
    """
    Embeds selected log messages for semantic retrieval using OpenAI embeddings.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=log_messages,
        model="text-embedding-3-small"
    )
    return [embedding.embedding for embedding in response.data]
