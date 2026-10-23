from sentence_transformers import SentenceTransformer


def embed_translation_memory(text):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embedding = model.encode(text)
    return embedding
