from typing import List, Tuple

from safety_client import build_client, moderate_with_openai, get_response_item
from safety_models import ModerationRequest, normalize_text


def redact_unsafe(request: ModerationRequest) -> Tuple[str, List[Tuple[int, int]]]:
    client = build_client()
    text = normalize_text(request.text)
    response = moderate_with_openai(client, [text])
    item = get_response_item(response, 0)
    spans = []
    for span in getattr(item, "category_applied_input_types", {}) or {}:
        spans.append((0, len(text)))
    if getattr(item, "flagged", False):
        return "[REDACTED]", spans or [(0, len(text))]
    return text, spans
