# Embed moderation rationales for case retrieval
from sentence_transformers import SentenceTransformer


def embed_moderation_reason(reason: str) -> List[float]:
    """Embed moderation rationale using Sentence Transformers (all-MiniLM-L6-v2)."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(reason, convert_to_tensor=False)
    return embedding.tolist()