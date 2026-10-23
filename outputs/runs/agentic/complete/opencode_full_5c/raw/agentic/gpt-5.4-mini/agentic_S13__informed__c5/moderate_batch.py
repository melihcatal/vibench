from safety_client import get_client
from safety_models import (
    BatchModerationResult,
    ModerationRequest,
    ModerationResult,
    normalize_text,
)


def moderate_batch(messages):
    client = get_client()
    results = []
    for message in messages:
        request = ModerationRequest(text=normalize_text(message))
        raw = client.post(
            "/contentsafety/text:analyze?api-version=2024-09-01", {"text": request.text}
        )
        results.append(
            ModerationResult(
                flagged=bool(raw.get("blocklistsMatch", False))
                or bool(raw.get("hateResult", {}).get("filtered", False)),
                categories=[],
                raw=raw,
            )
        )
    return BatchModerationResult(results=results)
