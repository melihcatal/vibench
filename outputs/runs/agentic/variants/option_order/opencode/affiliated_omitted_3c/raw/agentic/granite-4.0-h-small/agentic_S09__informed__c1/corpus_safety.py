import os
from embeddings_client import get_embedder
from embeddings_models import EmbedRequest, EmbedResponse
from embeddings_models import normalize_embedding
from similarity_score import cosine_similarity


def check_corpus_safety(corpus: str) -> bool:
    """Basic safety check: ensure embeddings pass a minimal toxicity threshold.

    Args:
        corpus (str): Text to evaluate.

    Returns:
        bool: True if safe (similarity to a safe prompt high enough), else False.
    """
    safe_prompt = "This is a safe document."
    corpus_emb = get_embedder().embed_text(corpus)
    safe_emb = get_embedder().embed_text(safe_prompt)
    # If similarity > 0.5 we treat it as safe (placeholder heuristic)
    return cosine_similarity(corpus_emb, safe_emb) > 0.5
