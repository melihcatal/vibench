# LATER-STEP implementation - Embeds transcript segments for semantic retrieval using Watsonx.ai embeddings

import os
from ibm_watsonx_ai import watsonx
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Provider identifier
PROVIDER = "IBM Slate Embeddings"

# Load API key and project ID from environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Authenticate with the embeddings service
authenticator = IAMAuthenticator(WATSONX_API_KEY)
client = watsonx(base_url="https://api.us-south.watsonx.ibm.com")
client.set_authenticator(authenticator)

# Use the Slate embeddings model
model_id = "slate-embedding-english-v3"


def transcript_embedding(segments):
    """Creates dense embeddings for each transcript segment.

    Args:
        segments (list): List of strings, each a segment of the transcript.

    Returns:
        dict: A mapping of segment index to its embedding vector (as list of floats).
    """
    embeddings = {}
    for idx, segment in enumerate(segments):
        resp = client.embedding(model=model_id, text=segment)
        vec = resp.get("result", [{}])[0].get("embedding")
        embeddings[idx] = vec  # list of floats
    return {"provider": PROVIDER, "embeddings": embeddings}
