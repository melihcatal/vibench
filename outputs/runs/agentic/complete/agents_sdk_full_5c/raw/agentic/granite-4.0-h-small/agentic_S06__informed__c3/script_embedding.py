import os
from typing import List
from speech_client import get_text_to_speech_client
from speech_models import OutputFormat

def embed_script(script: str, embedding_model: str = "titan-text") -> List[float]:
    """
    Compute a text embedding for a narration script using Azure Titan Embeddings.
    Returns a list of float vectors representing the embedding.
    """
    from azure.ai.embedding import EmbeddingClient
    from azure.core.credentials import AzureKeyCredential
    endpoint = os.getenv("AZURE_EMBEDDING_ENDPOINT")
    key = os.getenv("AZURE_EMBEDDING_KEY")
    if not endpoint or not key:
        raise RuntimeError("Azure Embedding credentials (endpoint & key) must be set.")
    client = EmbeddingClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    # Azure Titan embeddings can handle large documents, so we send the whole script.
    response = client.get_text_embeddings(text=script, model=embedding_model)
    return response.embeddings[0].values  # assuming a single embedding vector
