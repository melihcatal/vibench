import vertexai
from vertexai.preview.language_models import TextEmbeddingModel
import os
from typing import List

def embed_outputs(texts: List[str]) -> List[List[float]]:
    """Embeds model outputs for clustering or retrieval using Vertex AI."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    
    # The embed method returns a list of Embedding objects.
    # Each Embedding object has a 'values' attribute which is the list of floats.
    embeddings = model.embed(texts)
    
    return [embedding.values for embedding in embeddings]
