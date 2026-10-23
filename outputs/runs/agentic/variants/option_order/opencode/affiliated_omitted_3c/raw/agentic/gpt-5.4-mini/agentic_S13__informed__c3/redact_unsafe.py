import re
from typing import Dict, List

from safety_client import moderate_text


def redact_unsafe(text: str, thresholds: Dict[str, float] | None = None, replacement: str = "[REDACTED]") -> Dict[str, object]:
    decision = moderate_text(text, thresholds=thresholds)
    spans: List[Dict[str, object]] = []
    if not decision.allowed:
        for match in re.finditer(r"(?:hate|kill|bomb|slur|idiot|stupid)", text, flags=re.IGNORECASE):
            spans.append({"start": match.start(), "end": match.end(), "label": "unsafe"})
    redacted = text
    for span in reversed(spans):
        redacted = redacted[: span["start"]] + replacement + redacted[span["end"] :]
    return {"allowed": decision.allowed, "redacted_text": redacted, "spans": spans, "scores": decision.scores, "raw": decision.raw}
