import os
import cohere


def embed_translated_segment(
    original_text: str, translated_text: str, language_pair: str = "en-es"
) -> dict:
    """Embed translated segments for translation-memory search using Cohere API."""
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(cohere_api_key)

    response = co.embed(
        texts=[original_text, translated_text],
        model="embed-multilingual-v3.0",
        input_type="search_document",
    )

    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "language_pair": language_pair,
        "original_embedding": response.embeddings[0],
        "translated_embedding": response.embeddings[1],
        "model": "cohere/embed-multilingual-v3.0",
        "embedding_dimensions": len(response.embeddings[0]),
    }
