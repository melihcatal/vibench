# embed_batch.py
# [SAME-SCENARIO] Generates embeddings for a batch of texts

import os
from ibm_watsonx_ai.services import TextEmbeddings
from ibm_watsonx_ai import Client

# Load configuration from environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize client
client = Client(project_id=WATSONX_PROJECT_ID, api_key=WATSONX_API_KEY)
embeddings_service = TextEmbeddings(client=client)


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts.
    Args:
        texts (list[str]): List of text strings.
    Returns:
        list[list[float]]: List of embedding vectors as lists of floats.
    """
    response = embeddings_service.embed_text(
        project_id=WATSONX_PROJECT_ID, documents=texts, model_id="slate-125m-english-v1"
    )
    return response  # list of embeddings, each a list of floats
