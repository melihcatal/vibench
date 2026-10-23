from typing import List, Tuple

from safety_client import post_perspective
from safety_models import RedactionResult, normalize_text


def redact_unsafe(text: str) -> RedactionResult:
    content = normalize_text(text)
    payload = {
        "comment": {"text": content},
        "requestedAttributes": {
            "TOXICITY": {"spanAnnotations": True},
            "PROFANITY": {"spanAnnotations": True},
        },
        "doNotStore": True,
    }
    data = post_perspective(payload)
    spans: List[Tuple[int, int]] = []
    for attribute in data.get("attributeScores", {}).values():
        for span in attribute.get("spanScores", []):
            begin = int(span.get("begin", 0))
            end = int(span.get("end", 0))
            if end > begin:
                spans.append((begin, end))
    spans.sort()
    redacted = content
    for begin, end in reversed(spans):
        redacted = redacted[:begin] + "[REDACTED]" + redacted[end:]
    return RedactionResult(
        text=redacted, spans=[{"begin": b, "end": e} for b, e in spans]
    )
