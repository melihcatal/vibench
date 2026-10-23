from sentence_transformers import SentenceTransformer

def moderation_reason_embedding(text: str) -> List[float]:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding.tolist()