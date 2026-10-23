import os
import json

# Embed secret audit notes for semantic search
# Using IBM watsonx.ai embeddings as an example
import json
import uuid

from ibm_watsonx_ai.services import WatsonXaiEmbedding
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

authenticator = IAMAuthenticator(WATSONX_API_KEY)
embedding_service = WatsonXaiEmbedding(
    authenticator=authenticator, project_id=WATSONX_PROJECT_ID
)


def generate_embedding(note: str) -> str:
    """Create an embedding for a secret's audit note.",
    Returns the UUID of the stored embedding.
    """
    response = embedding_service.create_embedding(text=note)
    result = response.get_result()
    return result["embedding_id"]


if __name__ == "__main__":
    note = os.getenv("AUDIT_NOTE")
    if note:
        embedding_id = generate_embedding(note)
        print("Stored embedding ID:", embedding_id)
    else:
        print("Set AUDIT_NOTE env var")
