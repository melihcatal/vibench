import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hai.embeddings import EmbeddingServiceV2


def embed_output(text: str) -> list[float]:
    """Embed model output text using watsonx.ai text embeddings."""
    api_key = os.getenv("WATSONX_API_KEY", "<INSERT_WATSONX_API_KEY>")
    project_id = os.getenv("WATSONX_PROJECT_ID", "<INSERT_WATSONX_PROJECT_ID>")
    client = APIClient(
        api_key=api_key, project_id=project_id, url="https://api.watsonx.ai"
    )
    embedder = EmbeddingServiceV2(client)
    # Embed a single document; returns list of floats.
    embedding = embedder.create_embeddings(
        input_text=text, model_id="ibm/granite-20m-uncased"
    )
    return embedding.embedding
