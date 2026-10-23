
import os
import openai

def generate_embeddings_batch(texts: list[str], model: str = "text-embedding-ada-002") -> list[list[float]]:
    """
    Generates embeddings for a batch of texts using OpenAI's embedding model.

    Args:
        texts: A list of strings to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.Embedding.create(
        input=texts,
        model=model
    )
    return [data.embedding for data in response.data]
