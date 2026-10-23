import re


def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {"text": payload}
    if payload is None:
        return {"text": ""}
    if isinstance(payload, dict):
        text = payload.get("text", "")
        if text is None:
            text = ""
        return {**payload, "text": str(text)}
    return {"text": str(payload)}


def normalize_messages(payload):
    if isinstance(payload, dict) and "messages" in payload:
        messages = payload["messages"]
    else:
        messages = payload
    if messages is None:
        return []
    return [normalize_text_payload(message) for message in messages]


def extract_text(payload):
    normalized = normalize_text_payload(payload)
    return normalized["text"]


def redact_spans(text, spans):
    if not spans:
        return text
    pieces = []
    last = 0
    for span in sorted(spans, key=lambda item: item["start"]):
        start = max(0, int(span["start"]))
        end = max(start, int(span["end"]))
        pieces.append(text[last:start])
        pieces.append("[REDACTED]")
        last = end
    pieces.append(text[last:])
    return "".join(pieces)


def threshold_allows(scores, thresholds):
    for category, limit in thresholds.items():
        if scores.get(category, 0) >= limit:
            return False
    return True
