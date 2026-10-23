from sentence_transformers import SentenceTransformer


def embed_secret_audit_notes(notes):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(notes)
