from sentence_transformers import SentenceTransformer

def log_embedding(log_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(log_text)
    return embedding