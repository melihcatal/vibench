import os
from ibm_watsonx_ai.services import EmbEmbeddingsService


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding vector for a single text string using IBM Slate Embeddings.

    Args:
        text (str): The input text to embed.

    Returns:
        list[float]: The embedding vector as a list of floats.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    client = EmbEmbeddingsService(api_key=api_key, project_id=project_id)
    response = client.create_embed(text=text)
    # The API returns a list of floats in the 'embedding' field
    return response["embedding"]
