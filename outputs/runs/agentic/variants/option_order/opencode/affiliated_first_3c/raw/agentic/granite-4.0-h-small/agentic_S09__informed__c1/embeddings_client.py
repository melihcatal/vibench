import os
from pathlib import Path

# Configuration values (set environment variables)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


def create_client() -> "watsonx_ai.apis.EmbeddingsApi":
    """Create and return a configured IBM Watsonx embeddings client.

    Returns:
        Configured EmbeddingsApi instance.
    """
    from ibm_watsonx_ai.apis import EmbeddingsApi
    from ibm_watsonx_ai.client import APIClient

    # Initialize the IBM Watsonx client library with authentication
    apiclient = APIClient(
        api_key=WATSONX_API_KEY,
        project_id=WATSONX_PROJECT_ID,
        url="https://api.watsonx.ai",  # base URL for IBM Watsonx
    )
    return EmbeddingsApi(apiclient)


# Helper to convert raw API response to a simple list of embedding vectors
def normalize_response(response) -> list[list[float]]:
    """Normalize the provider's embedding response into a list of float vectors.

    Args:
        response: API response payload returned by the provider.
    """
    # IBM Watsonx returns a list of embeddings under 'embeddings' key
    return [emb.values for emb in response["embeddings"]]
