from sentence_transformers import SentenceTransformer


def embed_text(text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(text)
    return embedding
