from embed_text import embed_text
from embeddings_models import SimilarityResult, cosine_similarity


def similarity_score(text_a, text_b, model=None, dimensions=None, api_key=None):
    resp_a = embed_text(text_a, model=model, dimensions=dimensions, api_key=api_key)
    resp_b = embed_text(text_b, model=model, dimensions=dimensions, api_key=api_key)
    score = cosine_similarity(resp_a.embedding, resp_b.embedding)
    return SimilarityResult(
        score=score,
        text_a=text_a,
        text_b=text_b,
        vector_a=resp_a.embedding,
        vector_b=resp_b.embedding,
    )
