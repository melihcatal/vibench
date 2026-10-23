import os
from ibm_watsonx_ai.services import EmbEmbeddingsService


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a batch of text strings using IBM Slate Embeddings.

    Args:
        texts (list[str]): List of texts to embed.

    Returns:
        list[list[float]]: A list of embedding vectors, each a list of floats.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    client = EmbEmbeddingsService(api_key=api_key, project_id=project_id)
    response = client.create_embed(text=texts)
    # Response contains a list of embedding vectors
    return [vec["embedding"] for vec in response]
