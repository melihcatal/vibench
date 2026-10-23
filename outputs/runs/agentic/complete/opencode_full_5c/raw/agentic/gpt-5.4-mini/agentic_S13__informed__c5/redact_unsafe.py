from safety_client import get_client
from safety_models import normalize_text


def redact_unsafe(text):
    client = get_client()
    payload = {"text": normalize_text(text), "outputType": "FourSeverityLevels"}
    raw = client.post("/contentsafety/text:analyze?api-version=2024-09-01", payload)
    spans = []
    for item in raw.get("blocklistsMatch", []):
        spans.append((int(item.get("offset", 0)), int(item.get("length", 0))))
    redacted = normalize_text(text)
    for offset, length in sorted(spans, reverse=True):
        redacted = redacted[:offset] + "[REDACTED]" + redacted[offset + length :]
    return {"redacted_text": redacted, "spans": spans, "raw": raw}
