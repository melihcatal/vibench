from __future__ import annotations

from safety_client import moderate_text_request
from safety_models import BatchModerationResult, ModerationRequest, batch_result_to_dict


def moderate_messages(
    messages: list[str],
    language: str | None = None,
    threshold: float = 0.7,
) -> dict:
    results = [
        moderate_text_request(
            ModerationRequest(text=message, language=language), threshold=threshold
        )
        for message in messages
    ]
    batch = BatchModerationResult(results=results, provider="Perspective API")
    return batch_result_to_dict(batch)
