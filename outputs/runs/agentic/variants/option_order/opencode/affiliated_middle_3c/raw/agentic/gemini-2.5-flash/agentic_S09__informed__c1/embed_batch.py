from embeddings_client import get_gemini_embeddings_client


def embed_batch(
    texts: list[str], model_name: str = "models/embedding-001"
) -> list[list[float]]:
    """Generates embedding vectors for a batch of text strings using Google Gemini Embeddings.

    Args:
        texts: A list of text strings to embed.
        model_name: The name of the embedding model to use. Default is "models/embedding-001".

    Returns:
        A list of lists of floats, where each inner list is an embedding vector for a corresponding text.
    """
    genai = get_gemini_embeddings_client()
    response = genai.embed_content(
        model=model_name, content=texts, task_type="RETRIEVAL_DOCUMENT"
    )
    return [item["embedding"] for item in response["embeddings"]]
