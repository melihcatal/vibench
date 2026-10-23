from __future__ import annotations

from safety_client import moderate_text_request
from safety_models import ModerationRequest, RedactionSpan, moderation_result_to_dict


def flag_or_redact_unsafe_spans(
    text: str,
    threshold: float = 0.8,
    replacement: str = "[UNSAFE]",
) -> dict:
    result = moderate_text_request(ModerationRequest(text=text), threshold=threshold)
    spans: list[RedactionSpan] = []
    redacted_text = text
    if result.blocked:
        spans.append(
            RedactionSpan(
                start=0, end=len(text), label="unsafe_text", replacement=replacement
            )
        )
        redacted_text = replacement
    payload = moderation_result_to_dict(result)
    payload["redacted_text"] = redacted_text
    payload["spans"] = [span.__dict__ for span in spans]
    return payload
