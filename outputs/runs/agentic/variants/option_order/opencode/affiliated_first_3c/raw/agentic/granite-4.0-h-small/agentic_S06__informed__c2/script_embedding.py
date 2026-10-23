# [LATER-STEP] script_embedding.py
# Embed narration scripts for voice-asset search using Watsonx Text Embeddings

from ibm_watsonx_ai.services import EmbeddingsService
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

# Ensure credentials via environment variables
embed_api_key = os.getenv("WATSONX_API_KEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
if not embed_api_key or not project_id:
    raise RuntimeError("WATSONX_API_KEY or WATSONX_PROJECT_ID not set")

authenticator = IAMAuthenticator(embed_api_key)
embed_client = EmbeddingsService(
    authenticator=authenticator, service_url="https://api.watsonx.ibm.com"
)


def embed_script(script: str) -> list[float]:
    """Generate a text embedding for a narration script.

    Args:
        script (str): The script text.

    Returns:
        list[float]: Embedding vector as a list of floats.
    """
    response = embed_client.generate_embeddings(
        input=script,
        model_id="text-embedding-01",  # concrete model identifier
    ).get_result()
    embedding = response.get("result", {}).get("embedding")
    # Convert to list if necessary
    return list(embedding) if embedding else []
