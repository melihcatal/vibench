# Embed model output using IBM Watsonx.ai Text Embeddings SDK

import os
from ibm_watson import NaturalLanguageService
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from model_client import normalize_response

# -------------------------------------------------
# IBM Watsonx.ai Embeddings configuration
# -------------------------------------------------
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

authenticator = IAMAuthenticator(WATSONX_API_KEY)
service = NaturalLanguageService(
    authenticator=authenticator,
    service_url=f"https://{WATSONX_PROJECT_ID}.api.watsonx.ibm.com",
)


def embed_text(text: str) -> list[float]:
    """Embed a piece of text using IBM Watsonx.ai embeddings API."""
    response = service.embeddings(
        input=text, model_id="text-embedding-ada-002"
    ).get_result()
    # The response contains a list of embedding vectors
    vectors = response.get("embeddings", [])
    # Return the first vector as a list of floats
    if vectors:
        return vectors[0]["embedding"]
    return []


# Example usage (uncomment to test)
# vec = embed_text("Hello, world!")
# print(vec)
