import os
import google.generativeai as genai
from embeddings_client import get_embeddings_client
from embeddings_models import EmbeddingBatchResponse


def embed_batch(texts: list[str]) -> EmbeddingBatchResponse:
    """
    Generates embedding vectors for a batch of text strings using Google Gemini Embeddings.
    """
    client = get_embeddings_client()
    model = "models/embedding-001"
    response = client.embed_content(model=model, content=texts)
    # The API returns a list of embeddings, one for each text in the batch
    embeddings = [item["embedding"] for item in response["embeddings"]]
    return EmbeddingBatchResponse(embeddings=embeddings)
