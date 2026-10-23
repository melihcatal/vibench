import os
import vertexai
from vertexai.language_models import TextEmbeddingModel
from typing import List, Dict, Any

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

def embed_platform_outputs(texts: List[str]) -> List[List[float]]:
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # Use TextEmbeddingModel specifically for embedding tasks
    # 'text-embedding-004' is a concrete model identifier for Vertex AI embeddings.
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    # The get_embeddings method takes a list of strings
    embeddings_response = model.get_embeddings(texts)

    # Extract the actual embedding vectors
    embeddings = [embedding.values for embedding in embeddings_response]
    return embeddings