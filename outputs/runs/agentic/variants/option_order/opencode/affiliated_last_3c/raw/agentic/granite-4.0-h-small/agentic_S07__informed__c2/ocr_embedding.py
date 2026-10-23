import os
from dashscope import (
    TextEmbedding,
)  # DashScope Embeddings – identifies the concrete provider


def embed_document_sections(
    text: str, model: str = "text-embedding-003-large"
) -> List[float]:
    """Generate embeddings for document sections using DashScope.

    Args:
        text (str): Plain text extracted from OCR; can be a whole document or a chunk.
        model (str): Model identifier for the embedding API (default: large model).

    Returns:
        List[float]: Embedding vector (list of floats).
    """
    # Environment variable holds DashScope API key
    client = TextEmbedding(api_key=os.getenv("DASHSCOPE_API_KEY"))
    # Generate embedding; the SDK returns a dict with 'embedding' field containing a list
    response = client.embed(model=model, text=text)
    return response["embedding"]
