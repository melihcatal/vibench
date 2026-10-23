# LATER-STEP: Embed moderation rationales for retrieval

from safety_client import get_client
from safety_models import ModerationResult
import sentence_transformers  # Concrete provider: Sentence-Transformers (e.g., all-MiniLM-L6-v2)

model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")


def embed_reasons(result: ModerationResult) -> list[float]:
    """Return an embedding of the moderation rationale.

    Uses the textual reason (if any) returned by the moderation service.
    """
    # OpenAI moderation may include a 'detail' field; fallback to category list.
    rationale = result.get("detail") or str(result["categories"])
    embedding = model.encode([rationale], convert_to_tensor=True)[0].tolist()
    return embedding
