import cohere
import os


def embed_secret_audit_notes(audit_notes):
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=[audit_notes], model="embed-english-v3.0")
    return response.embeddings[0]
