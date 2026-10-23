import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a batch of text strings using Google's Vertex AI.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_REGION")
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.embed_documents(texts)
    return [embedding.values for embedding in embeddings]
