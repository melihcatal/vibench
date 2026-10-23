import os
from typing import Tuple

# Watsonx embeddings client import (concrete provider signal)
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmbeddingsOptions

# Environment variables for authentication
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_URL = os.getenv("WATSONX_URL", "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com")

if not WATSONX_APIKEY:
    raise RuntimeError("Set WATSONX_APIKEY environment variable")

nlu = NaturalLanguageUnderstandingV1(
    version="2023-08-01",
    authenticator=IAMAuthenticator(WATSONX_APIKEY),
    service_url=WATSONX_URL,
)

def embed_script(text: str) -> Tuple[list, str]:
    """Generate dense vector embeddings for a narration script using Watsonx.

    Args:
        text: Raw narration script (plain text or SSML).

    Returns:
        (embedding_array, model_id) where embedding_array is a list of floats.
    """
    # Extract plain text from possible SSML tags
    clean_text = re.sub(r"<[^>]+>", " ", text).strip()
    response = nlu.embed_content(
        body={
            "text": clean_text,
        },
        features=Features(embeddings=EmbeddingsOptions(model="ibm-embedder")),
    ).get_result()
    # The API returns embeddings as a list of floats under 'embeddings'
    embeddings = response.get("embeddings", [])
    model_id = response.get("model_id", "unknown")
    return embeddings, model_id

if __name__ == "__main__":
    sample = "This is a sample narration that will be embedded for voice search."
    vec, model = embed_script(sample)
    print(f"Embedded with model {model}: {vec[:5]}... (total {len(vec)} dims)")
