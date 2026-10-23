from sentence_transformers import SentenceTransformer


def embed_text(text: str) -> list:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding.tolist()

