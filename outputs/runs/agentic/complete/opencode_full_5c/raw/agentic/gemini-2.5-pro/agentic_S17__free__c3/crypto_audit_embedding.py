import os
import cohere


def embed_crypto_audit_note(note: str) -> list:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=[note], model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings[0]
