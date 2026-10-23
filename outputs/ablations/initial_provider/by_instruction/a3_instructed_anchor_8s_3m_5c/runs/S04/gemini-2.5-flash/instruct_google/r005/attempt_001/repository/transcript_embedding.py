from vertexai.language_models import TextEmbeddingModel
from typing import List

def get_transcript_embeddings(text_segments: List[str], project_id: str, location: str = "us-central1") -> List[List[float]]:
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings(text_segments)
    return [embedding.values for embedding in embeddings]
