from sentence_transformers import SentenceTransformer


def embed_script(script):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(script)
    return embedding
