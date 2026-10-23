from typing import List, Dict, Any
from vertexai.language_models import TextEmbeddingInput


def prepare_texts_for_embedding(texts: List[str]) -> List[TextEmbeddingInput]:
    """
    Prepares a list of text strings into the format required by the Vertex AI embedding model.
    Each text is treated as a SEMANTIC_SIMILARITY task.
    """
    return [TextEmbeddingInput(text, "SEMANTIC_SIMILARITY") for text in texts]


def normalize_embedding_response(response: Any) -> List[List[float]]:
    """
    Normalizes the embedding response from Vertex AI into a list of embedding vectors.
    """
    return [embedding.values for embedding in response.embeddings]
