from embeddings_client import cosine_similarity, embed_texts


def score_similarity(text_a: str, text_b: str) -> float:
    embeddings = embed_texts([text_a, text_b]).embeddings
    return cosine_similarity(embeddings[0], embeddings[1])
