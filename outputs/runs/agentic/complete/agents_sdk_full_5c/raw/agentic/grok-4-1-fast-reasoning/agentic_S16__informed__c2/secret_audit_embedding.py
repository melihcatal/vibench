import cohere
import os

def embed_secret_audit_notes(notes: str) -> list[float]:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=[notes],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings[0]