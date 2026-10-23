from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def embed_audit_notes(notes):
    return model.encode(notes)