from embeddings_client import embed_single, normalize_embedding
from embeddings_models import cosine_similarity


def similarity_score(text1: str, text2: str) -> float:
    emb1 = normalize_embedding(embed_single(text1))
    emb2 = normalize_embedding(embed_single(text2))
    return cosine_similarity(emb1, emb2)
