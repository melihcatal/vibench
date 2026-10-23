import os
from ibm_watsonx_ai.embeddings import EmbeddingClient
from model_client import get_llm_client

def embed_text(text: str) -> list[float]:
    """Generate an embedding for the given text using IBM Slate embeddings.\n    Returns a list of float values."""
    client = EmbeddingClient(api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID"))
    response = client.create_embedding(input=text)
    # Assuming response contains 'embedding' as a list of floats
    return response['embedding']
