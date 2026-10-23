from sentence_transformers import SentenceTransformer

def moderation_reason_embedding(reason):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding = model.encode(reason)
    return embedding