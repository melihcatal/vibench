from sentence_transformers import SentenceTransformer


def embed_log_message(log_message):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(log_message)
    return embedding.tolist()