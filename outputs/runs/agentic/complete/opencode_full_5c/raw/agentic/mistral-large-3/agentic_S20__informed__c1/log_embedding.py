import os
from cohere import Client
from typing import List


def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    """
    Embeds selected log messages for semantic retrieval using Cohere's Embed API.

    Args:
        log_messages: List of log message strings to embed.

    Returns:
        List of embedding vectors for the log messages.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    client = Client(api_key=api_key)

    response = client.embed(
        texts=log_messages, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
