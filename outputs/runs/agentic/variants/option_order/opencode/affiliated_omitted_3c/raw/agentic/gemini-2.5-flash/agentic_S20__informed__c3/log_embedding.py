import os
from openai import OpenAI
from typing import List


def embed_log_messages(
    log_messages: List[str], model: str = "text-embedding-ada-002"
) -> List[List[float]]:
    """Embeds selected log messages for semantic retrieval using OpenAI Embeddings.

    Args:
        log_messages: A list of log message strings to embed.
        model: The OpenAI embedding model to use (default: text-embedding-ada-002).

    Returns:
        A list of embedding vectors, one for each log message.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.embeddings.create(input=log_messages, model=model)
        return [data.embedding for data in response.data]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []
