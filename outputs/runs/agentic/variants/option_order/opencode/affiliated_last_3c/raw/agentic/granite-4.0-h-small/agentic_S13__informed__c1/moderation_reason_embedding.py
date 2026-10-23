import json
from safety_models import build_request, normalize_response
from safety_client import analyze_sentiment


def embed_reason(reason_text: str) -> Dict[str, Any]:
    """Embed moderation rationale for downstream case retrieval.

    Uses a hosted embedding model (e.g., Anthropic embeddings) to turn a free‑form
    moderation explanation into a vector suitable for similarity search.
    """
    request = build_request(reason_text)
    raw = analyze_sentiment(reason_text)  # placeholder for embedding call
    # Example: replace with your embedding service SDK call
    embedding = raw.get("embedding")  # list of floats
    return {"embedding": embedding, "raw": reason_text}
