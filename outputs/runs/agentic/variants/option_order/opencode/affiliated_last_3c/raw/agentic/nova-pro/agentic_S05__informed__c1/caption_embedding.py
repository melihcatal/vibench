from sentence_transformers import SentenceTransformer


def caption_embedding(text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(text)
    return embedding
