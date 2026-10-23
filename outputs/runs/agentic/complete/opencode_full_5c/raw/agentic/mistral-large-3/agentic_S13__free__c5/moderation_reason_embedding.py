from typing import Dict, Any, List
from sentence_transformers import SentenceTransformer


def moderation_reason_embedding(reasons: List[str]) -> Dict[str, Any]:
    """
    Embeds moderation rationales for case retrieval using Sentence Transformers (all-MiniLM-L6-v2).
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(reasons, convert_to_tensor=True)

    return {
        "reasons": reasons,
        "embeddings": embeddings.tolist(),
        "model": "all-MiniLM-L6-v2",
    }
