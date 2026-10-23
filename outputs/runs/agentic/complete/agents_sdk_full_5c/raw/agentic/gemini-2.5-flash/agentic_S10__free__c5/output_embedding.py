from typing import List
from vertexai.preview.language_models import TextEmbeddingModel

from model_client import get_embedding_model

def embed_text(texts: List[str]) -> List[List[float]]:
    model = get_embedding_model()
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]
