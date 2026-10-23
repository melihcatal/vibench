from sentence_transformers import SentenceTransformer


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding = model.encode(payload['text'])
    return {'embedding': embedding.tolist()}