from embeddings_client import get_gemini_embeddings_client


def embed_text(text: str, model_name: str = "models/embedding-001") -> list[float]:
    """Generates an embedding vector for a single text string using Google Gemini Embeddings.

    Args:
        text: The text string to embed.
        model_name: The name of the embedding model to use. Default is "models/embedding-001".

    Returns:
        A list of floats representing the embedding vector.
    """
    genai = get_gemini_embeddings_client()
    response = genai.embed_content(
        model=model_name, content=text, task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]
