from safety_client import get_client
from safety_models import (
    ModerationCategory,
    ModerationRequest,
    ModerationResult,
    normalize_text,
)


def moderate_text(text, language=None):
    request = ModerationRequest(text=normalize_text(text), language=language)
    client = get_client()
    payload = {"text": request.text, "language": request.language}
    raw = client.post("/contentsafety/text:analyze?api-version=2024-09-01", payload)
    categories = []
    for item in raw.get("categoriesAnalysis", []):
        categories.append(
            ModerationCategory(
                name=item.get("category", "unknown"),
                score=float(item.get("severity", 0.0)),
                flagged=bool(item.get("isFiltered", False)),
            )
        )
    return ModerationResult(
        flagged=bool(raw.get("blocklistsMatch", False))
        or any(c.flagged for c in categories),
        categories=categories,
        raw=raw,
    )
