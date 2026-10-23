# embed_text.py
# [SAME-SCENARIO] Generates an embedding vector for one text string

import os
from ibm_watsonx_ai.services import TextEmbeddings
from ibm_watsonx_ai import Client

# Load configuration from environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize the client
client = Client(project_id=WATSONX_PROJECT_ID, api_key=WATSONX_API_KEY)
embeddings_service = TextEmbeddings(client=client)


def embed_text(text: str) -> list[float]:
    """Generate embedding for a single text string.
    Args:
        text (str): The input text.
    Returns:
        list[float]: Embedding vector as a list of floats.
    """
    response = embeddings_service.embed_text(
        project_id=WATSONX_PROJECT_ID,
        documents=[text],
        model_id="slate-125m-english-v1",
    )
    # The API returns a list of embeddings, each as a list of floats
    return response[0]
