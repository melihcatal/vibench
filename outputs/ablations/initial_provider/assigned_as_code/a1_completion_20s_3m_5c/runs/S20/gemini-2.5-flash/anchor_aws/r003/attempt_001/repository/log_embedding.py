import os
from typing import List, Dict, Any
from google.cloud import aiplatform

from observability_models import EmbeddingRequest

def embed_log_messages(request: EmbeddingRequest, project_id: str, location: str = "us-central1") -> List[List[float]]:
    aiplatform.init(project=project_id, location=location)

    # Using a specific embedding model from Vertex AI. text-embedding-004 is a common choice.
    model_id = os.environ.get("VERTEX_AI_EMBEDDING_MODEL_ID", "text-embedding-004")
    model = aiplatform.private_preview.language_models.TextEmbeddingModel.from_pretrained(model_id)

    # Generate embeddings for the provided texts
    embeddings = model.predict(request.text)
    
    # The embeddings are typically returned as a list of lists of floats
    return embeddings.embeddings
