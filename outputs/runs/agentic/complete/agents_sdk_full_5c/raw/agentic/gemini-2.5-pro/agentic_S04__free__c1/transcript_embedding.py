from typing import List
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

def embed_text_segments(
    project_id: str,
    location: str,
    text_segments: List[str]
) -> List[List[float]]:
    """
    Generates embeddings for a list of text segments using Google Vertex AI.
    """
    aiplatform.init(project=project_id, location=location)
    
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    embeddings = model.get_embeddings(text_segments)
    
    return [embedding.values for embedding in embeddings]
