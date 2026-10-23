import cohere
import os

def secret_audit_embedding(audit_notes: str) -> list:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=[audit_notes],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings[0]