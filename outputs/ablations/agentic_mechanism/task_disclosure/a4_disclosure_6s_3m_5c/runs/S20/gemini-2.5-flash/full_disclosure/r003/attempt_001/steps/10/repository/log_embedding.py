import os
import openai

def embed_log_messages(log_messages: list[str]) -> list[list[float]]:
    """
    Embeds selected log messages for semantic retrieval using OpenAI.

    Args:
        log_messages: A list of log messages to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()
    model = "text-embedding-ada-002"

    response = client.embeddings.create(
        input=log_messages,
        model=model
    )
    return [item.embedding for item in response.data]
