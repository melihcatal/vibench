from sentence_transformers import SentenceTransformer


def moderation_reason_embedding(text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding.tolist()