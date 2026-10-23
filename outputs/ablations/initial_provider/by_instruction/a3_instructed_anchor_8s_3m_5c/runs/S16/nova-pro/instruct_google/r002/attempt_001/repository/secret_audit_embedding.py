from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_secret_audit_notes(notes):
    return model.encode(notes)