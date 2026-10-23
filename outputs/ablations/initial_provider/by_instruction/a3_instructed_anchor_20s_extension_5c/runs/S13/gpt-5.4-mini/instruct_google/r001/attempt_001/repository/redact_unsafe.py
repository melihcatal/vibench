from safety_client import get_threshold
from safety_models import normalize_text


def redact_unsafe(text, unsafe_spans=None):
    content = normalize_text(text)
    spans = unsafe_spans or []
    chars = list(content)
    threshold = get_threshold()
    for span in spans:
        start = int(span.get("start", 0))
        end = int(span.get("end", 0))
        score = float(span.get("score", 1.0))
        if score >= threshold:
            for i in range(max(0, start), min(len(chars), end)):
                chars[i] = "[REDACTED]"
    return "".join(chars)
