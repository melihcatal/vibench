from vertexai.preview.language_models import TextEmbeddingModel

def embed_text(text: str) -> list[float]:
    """
    Embeds text using Google Cloud Vertex AI's TextEmbeddingModel.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding.
    """
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
