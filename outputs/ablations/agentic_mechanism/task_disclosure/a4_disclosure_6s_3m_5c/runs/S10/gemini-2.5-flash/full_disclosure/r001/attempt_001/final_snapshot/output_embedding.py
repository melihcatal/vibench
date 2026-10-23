from typing import List

import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def embed_text(texts: List[str]) -> List[List[float]]:
    """Embeds a list of texts using a Vertex AI embedding model.

    Args:
        texts: A list of strings to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1")
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in texts]
    embeddings = model.get_embeddings(inputs)
    return [embedding.values for embedding in embeddings]
