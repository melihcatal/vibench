import os
from typing import List
import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def get_batch_embeddings_vertexai(texts: List[str], project_id: str = None, location: str = "us-central1", model_name: str = "text-embedding-004") -> List[List[float]]:
    project_id = project_id if project_id else os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
    
    vertexai.init(project=project_id, location=location)
    
    model = TextEmbeddingModel.from_pretrained(model_name)
    
    embeddings_response = model.get_embeddings(texts)
        
    embeddings = [e.values for e in embeddings_response]
    return embeddings
