import re


def _text(value):
    return "" if value is None else str(value)


def normalize_text_payload(payload):
    if isinstance(payload, dict):
        text = payload.get("text", payload.get("content", ""))
    else:
        text = payload
    return {"text": _text(text)}


def normalize_batch_payload(payload):
    if isinstance(payload, dict):
        items = payload.get("messages", payload.get("texts", payload.get("items", [])))
    else:
        items = payload
    normalized = []
    for item in items or []:
        if isinstance(item, dict):
            normalized.append({"text": _text(item.get("text", item.get("content", "")))})
        else:
            normalized.append({"text": _text(item)})
    return {"messages": normalized}


def normalize_thresholds(payload):
    if isinstance(payload, dict):
        return {
            "text": _text(payload.get("text", payload.get("content", ""))),
            "thresholds": payload.get("thresholds", payload.get("categories", {})) or {},
        }
    return {"text": _text(payload), "thresholds": {}}


def redact_spans(text, spans):
    result = _text(text)
    for span in sorted(spans or [], key=lambda s: int(s.get("start", 0)), reverse=True):
        start = max(0, int(span.get("start", 0)))
        end = max(start, int(span.get("end", start)))
        result = result[:start] + "[REDACTED]" + result[end:]
    return result


def extract_text_field(item):
    if isinstance(item, dict):
        return _text(item.get("text", item.get("content", "")))
    return _text(item)


def parse_allowed_flag(score, threshold):
    try:
        return float(score) < float(threshold)
    except Exception:
        return False


def normalize_language(value):
    text = _text(value).strip().lower()
    if not text:
        return "en"
    return re.sub(r"[^a-z0-9-]", "", text)
