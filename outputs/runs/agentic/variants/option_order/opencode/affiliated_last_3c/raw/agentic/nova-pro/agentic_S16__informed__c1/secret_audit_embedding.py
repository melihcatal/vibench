from sentence_transformers import SentenceTransformer


def embed_secret_audit_notes(notes):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embeddings = model.encode(notes)
    return embeddings.tolist()
