# moderation_reason_embedding.py

import os
from ibm_watsonx_ai.hlp.embed import EmbeddingsClient  # watsonx.ai text embeddings SDK
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Provider identifiers (make the provider identifiable in code)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Utility to build an embedding of a moderation rationale


def embed_rationale(rationale: str) -> list[float]:
    """Return a list of floats representing the embedding of the given rationale.
    Uses Watsonx.ai's text embedding endpoint (HLP endpoint)."""
    authenticator = IAMAuthenticator(apikey=WATSONX_API_KEY)
    client = EmbeddingsClient(
        endpoint="https://api.us-south.watsonx.ibm.com",
        project_id=WATSONX_PROJECT_ID,
        auth_authenticator=authenticator,
    )
    # Use the default model for embeddings (e.g., ibm/granite-3-embed-0907-32k)
    response = client.embed(text=rationale)
    # The response format is typically: {"embeddings": [float, float, ...]}
    return response["embeddings"]


# Example usage (for local testing)
if __name__ == "__main__":
    rationale = "User posted hate speech targeting a protected group."
    vec = embed_rationale(rationale)
    print("Embedding size:", len(vec))
    print("First 5 values:", vec[:5])
