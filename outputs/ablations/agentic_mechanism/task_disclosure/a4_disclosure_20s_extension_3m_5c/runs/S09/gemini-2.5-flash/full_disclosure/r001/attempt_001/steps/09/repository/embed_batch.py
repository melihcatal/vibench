import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embeddings for a batch of texts using Google's TextEmbeddingModel.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]

