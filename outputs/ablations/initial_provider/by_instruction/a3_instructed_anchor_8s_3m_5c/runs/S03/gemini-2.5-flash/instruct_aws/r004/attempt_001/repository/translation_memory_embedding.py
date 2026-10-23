from google.cloud import aiplatform
from google.cloud.aiplatform.language_models import TextEmbeddingModel
from typing import List

def generate_translation_memory_embedding(text_segments: List[str], project_id: str, location: str = "us-central1") -> List[List[float]]:
    """
    Generates embeddings for translated segments for translation-memory search
    to find similar translated content using Google Cloud Vertex AI Embeddings.
    """
    aiplatform.init(project=project_id, location=location)

    # Use the TextEmbeddingModel from the high-level SDK
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")

    embeddings = model.get_embeddings(text_segments)

    # The get_embeddings method returns a list of TextEmbedding objects.
    # Each TextEmbedding object has an attribute `values` which is a list of floats.
    return [embedding.values for embedding in embeddings]
