import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google's Vertex AI.

    Args:
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    vertexai.init()
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

