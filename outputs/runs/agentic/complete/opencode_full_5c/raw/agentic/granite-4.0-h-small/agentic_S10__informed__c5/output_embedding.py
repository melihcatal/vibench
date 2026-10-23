import os
from google.genai.services.embeddings.slate import EmbeddingServiceClient
from model_models import LLMResponse


def embed_text(text: str) -> list[float]:
    """Embeds text using watsonx.ai Slate Embeddings.

    Returns a list of embedding floats.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError("WATSONX_API_KEY or WATSONX_PROJECT_ID not set")

    client = EmbeddingServiceClient(project=project_id, api_key=api_key)
    response = client.embed_content(text=text)
    # Assuming response returns a list of vectors under 'embeddings' key
    embeddings = response.get("embeddings")
    if not embeddings:
        raise ValueError("Embedding response missing 'embeddings' field")
    return embeddings
