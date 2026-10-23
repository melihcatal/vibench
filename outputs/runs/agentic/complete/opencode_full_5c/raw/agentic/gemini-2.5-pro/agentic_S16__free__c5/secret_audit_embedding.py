import os
import cohere


def secret_audit_embedding(text: str) -> list[float]:
    """
    Embed secret audit notes for semantic search using Cohere.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    co = cohere.Client(cohere_api_key)

    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings[0]
