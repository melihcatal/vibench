import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.nlp import EmbeddingModel
from model_client import ManagedModelClient

def platform_output_embedding(text: str, model_id: str = 'embed-enu') -> Any:
    """Generate an embedding for a model output using IBM watsonx.ai embeddings service."""
    client = ManagedModelClient()  # uses IBM credentials configured via env vars
    embedding_model = EmbeddingModel(model_id=model_id)
    response = client.embeddings.create(embedding_model, text=text)
    return response.raw
