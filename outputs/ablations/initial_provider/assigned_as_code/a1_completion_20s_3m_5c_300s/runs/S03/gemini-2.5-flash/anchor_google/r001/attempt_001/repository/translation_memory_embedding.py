import os
from typing import Dict, Any, List
import vertexai
from vertexai.language_models import TextEmbeddingModel
from translation_client import get_project_id # Re-using for project ID
from translation_models import TranslationMemoryEmbeddingRequest, TranslationMemoryEmbeddingResponse

def embed_translation_segment(payload: TranslationMemoryEmbeddingRequest, config: Dict[str, Any] = None) -> TranslationMemoryEmbeddingResponse:
    config = config or {}
    project_id = config.get("project_id", get_project_id())
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # Vertex AI is typically regional

    vertexai.init(project=project_id, location=location)

    # Using a concrete model ID for text embeddings
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

    # The TextEmbeddingModel can embed a list of texts. Here we have a single text.
    embeddings = model.get_embeddings([payload.text])

    # Each embedding result contains a list of floats
    embedding_vector = embeddings[0].values

    return TranslationMemoryEmbeddingResponse(
        embedding=embedding_vector
    )
