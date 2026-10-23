import os
import vertexai
from vertexai.language_models import TextEmbeddingModel
from typing import List

def embed_audit_notes(audit_notes: List[str], project_id: str = None, location: str = None) -> List[List[float]]:
    if project_id is None:
        project_id = os.environ.get("GCP_PROJECT_ID")
    if location is None:
        location = os.environ.get("GCP_LOCATION", "us-central1")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings(audit_notes)
    return [embedding.values for embedding in embeddings]
