import os
import cohere


def embed_text(text: str):
    """
    Embeds platform outputs for evaluation or retrieval using Cohere.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings[0]
