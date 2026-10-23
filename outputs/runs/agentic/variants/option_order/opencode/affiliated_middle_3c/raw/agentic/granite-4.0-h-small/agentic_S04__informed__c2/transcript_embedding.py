import os
from typing import List, Dict

# Embedding utilities using IBM Granite embeddings via watsonx.ai SDK

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be defined")

from ibm_watsonx_ai.services import EmbeddingService
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(WATSONX_API_KEY)
embedding_service = EmbeddingService(
    service_url="https://api.us-south.watsonx.ibm.com",
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
    authenticator=authenticator,
)

# Simple helper to convert text to embedding vector


def embed_segments(segments: List[str]) -> List[List[float]]:
    """Embed a list of text segments using Granite embedding model."""
    # Use batch endpoint - model: granite-embed-xxl-12m
    response = embedding_service.embed_text(
        model_id="granite-embed-xxl-12m", input=segments, input_type="text"
    )
    embeddings = response.get("embeddings", [])
    # Return as list of float vectors
    return [vec for vec in embeddings]


# Example (not executed)
# vecs = embed_segments(['Hello world', 'How are you?'])
# print(vecs)
