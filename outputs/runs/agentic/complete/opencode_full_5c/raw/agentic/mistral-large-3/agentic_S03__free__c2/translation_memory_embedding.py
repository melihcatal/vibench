from typing import List, Dict
import numpy as np
from google.cloud import aiplatform
from google.cloud.aiplatform import MatchingEngineIndex
import os


def embed_translated_segments(texts: List[str]) -> List[List[float]]:
    """Embed translated segments for translation-memory search using Google Vertex AI."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@latest")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]
