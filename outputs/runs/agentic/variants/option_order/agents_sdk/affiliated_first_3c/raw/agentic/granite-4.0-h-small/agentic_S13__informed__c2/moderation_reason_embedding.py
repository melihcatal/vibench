# [LATER-STEP] moderation_reason_embedding.py

from embeddings_client import EmbeddingsClient
from safety_models import TextModerationResult, UnsafeSpan

CLIENT = EmbeddingsClient()

def embed_moderation_reasons(result: TextModerationResult, spans: List[UnsafeSpan]) -> str:
    """Create an embedding for the concatenation of moderation rationale and flagged spans.
    Returns the embedding vector as a JSON‑serializable list.
    """
    rationale = []
    for cat, score in result.detailed.items():
        if score > result.thresholds.get(cat, 0.5):
            rationale.append(f\"{cat}: {score}\")
    for span in spans:
        rationale.append(f\"flag {span.category} [{span.start}:{span.end}] score={span.score}\")
    text = ' '.join(rationale)
    embedding = CLIENT.embed(text=text)
    # Return as list for downstream numeric processing
    return embedding.tolist()
