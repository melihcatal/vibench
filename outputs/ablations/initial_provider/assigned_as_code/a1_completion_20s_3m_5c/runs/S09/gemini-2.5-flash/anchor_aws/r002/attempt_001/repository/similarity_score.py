from embeddings_models import cosine_similarity

def similarity_score(embedding1, embedding2):
    score = cosine_similarity(embedding1, embedding2)
    return {"similarity_score": float(score)}
