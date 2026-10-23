from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_log_message(log_message):
    embedding = model.encode(log_message)
    return embedding
