from openai import OpenAI
import os
from typing import List, Dict

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def log_embedding(messages: List[str]) -> List[List[float]]:
    """
    Embeds selected log messages for semantic retrieval using OpenAI's text-embedding-ada-002 model.

    Args:
        messages (List[str]): List of log messages to embed.

    Returns:
        List[List[float]]: List of embedding vectors for the input messages.
    """
    if not messages:
        return []

    # Call OpenAI Embeddings API
    response = client.embeddings.create(input=messages, model="text-embedding-ada-002")

    return [embedding.embedding for embedding in response.data]
