import vertexai
from vertexai.language_models import TextEmbeddingModel
import os
from typing import List

def embed_segments(segments: List[str], project_id: str, location: str) -> List[List[float]]:
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003") # Concrete Vertex AI model
    embeddings = model.get_embeddings(segments)
    return [embedding.values for embedding in embeddings]
