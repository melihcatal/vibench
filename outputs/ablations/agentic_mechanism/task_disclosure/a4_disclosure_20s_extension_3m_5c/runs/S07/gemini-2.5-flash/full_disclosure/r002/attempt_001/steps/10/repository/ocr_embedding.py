import os
from typing import List

from vertexai.language_models import TextEmbeddingModel
import vertexai

def embed_document_sections(document_sections: List[str]) -> List[List[float]]:
    """
    Embeds extracted document sections for semantic retrieval using Google Cloud Vertex AI.

    Args:
        document_sections: A list of strings, where each string is a document section.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(document_sections)
    return [embedding.values for embedding in embeddings]
