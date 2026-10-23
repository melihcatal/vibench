from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')


def secret_audit_embedding(payload):
    embedding = model.encode(payload['audit_note'])
    return {'embedding': embedding.tolist()}