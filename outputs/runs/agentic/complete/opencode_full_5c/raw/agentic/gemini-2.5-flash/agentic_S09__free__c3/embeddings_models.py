COHERE_EMBEDDING_MODEL = "embed-english-v3.0"
COHERE_SEARCH_MODEL = "embed-english-v3.0"


def extract_embeddings(response):
    """Extracts embeddings from a Cohere API response."""
    if response and hasattr(response, "embeddings"):
        return response.embeddings
    return []
