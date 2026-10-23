import os
from typing import List
from google.cloud import aiplatform
from translation_models import EmbeddingRequest, EmbeddingResponse

def create_text_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_id = os.environ.get("VERTEX_AI_EMBEDDING_MODEL_ID", "text-embedding-004")

    aiplatform.init(project=project_id, location=location)
    
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)
    
    embeddings = model.get_embeddings([request.text])
    
    if embeddings and embeddings[0].values:
        return EmbeddingResponse(embedding=embeddings[0].values)
    else:
        return EmbeddingResponse(embedding=[])