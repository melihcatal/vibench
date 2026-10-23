from sentence_transformers import SentenceTransformer


def embed_log_message(message):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(message)
    return embedding